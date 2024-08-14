from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Constants
CSV_FILE_PATH = 'arcade_sessions.csv'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
USERS = {
    'admin': {
        'password': generate_password_hash('password'),
        'role': 'admin'
    },
    'user': {
        'password': generate_password_hash('userpass'),
        'role': 'user'
    }
}
@app.route('/export_data', methods=['POST'])
def export_data():
    if 'export_csv' in request.form:
        # Generate and return CSV file
        pass
    elif 'export_excel' in request.form:
        # Generate and return Excel file
        pass

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_csv(file_path):
    return pd.read_csv(file_path, encoding='ISO-8859-1')

def preprocess_data(df):
    df['Created At'] = pd.to_datetime(df['Created At'], errors='coerce')
    return df

def filter_sessions(df):
    return df[df['Time'] != 60]

def filter_by_date(df, start_date, end_date):
    if start_date:
        df = df[df['Created At'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['Created At'] <= pd.to_datetime(end_date)]
    return df

def filter_by_goal(df, goals):
    if goals:
        df = df[df['Goal'].isin(goals)]
    return df

def search_data(df, query):
    return df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]

def create_pdf_report(plots, summary_stats):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add summary stats
    pdf.cell(200, 10, txt="Arcade Sessions Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total Sessions: {summary_stats['total_sessions']}", ln=True)
    pdf.cell(200, 10, txt=f"Average Session Time: {summary_stats['average_session_time']:.2f} minutes", ln=True)
    pdf.cell(200, 10, txt=f"Median Session Time: {summary_stats['median_session_time']:.2f} minutes", ln=True)
    pdf.cell(200, 10, txt=f"Total Elapsed Time: {summary_stats['total_elapsed_time']} minutes", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Sessions per Goal:", ln=True)
    for goal, count in summary_stats['sessions_per_goal'].items():
        pdf.cell(200, 10, txt=f"{goal}: {count}", ln=True)

    # Add plots as images
    for plot in plots:
        img_buffer = BytesIO()
        plot.write_image(img_buffer, format='png')
        img_buffer.seek(0)
        pdf.image(img_buffer, x=10, y=None, w=180)

    return pdf

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    df = read_csv(CSV_FILE_PATH)
    df = preprocess_data(df)
    goals = df['Goal'].unique()
    return render_template('index.html', goals=goals)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and check_password_hash(USERS[username]['password'], password):
            session['username'] = username
            session['role'] = USERS[username]['role']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/filter', methods=['POST'])
def filter_data():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    selected_goals = request.form.getlist('goals')
    search_query = request.form.get('search_query')
    
    df = read_csv(CSV_FILE_PATH)
    df = preprocess_data(df)
    df_filtered = filter_sessions(df)
    
    if start_date or end_date:
        df = filter_by_date(df, start_date, end_date)
        df_filtered = filter_by_date(df_filtered, start_date, end_date)

    if selected_goals:
        df = filter_by_goal(df, selected_goals)
        df_filtered = filter_by_goal(df_filtered, selected_goals)

    if search_query:
        df = search_data(df, search_query)
        df_filtered = search_data(df_filtered, search_query)

    if df.empty:
        return jsonify({'no_data': True})

    # Generate summary statistics
    summary_stats = {
        'total_sessions': len(df),
        'average_session_time': df['Time'].mean(),
        'median_session_time': df['Time'].median(),
        'total_elapsed_time': df['Elapsed'].sum(),
        'sessions_per_goal': df['Goal'].value_counts().to_dict()
    }

    # Generate plots
    plots = []
    plot_names = request.form.getlist('plot_options')

    if 'session_time_over_time' in plot_names:
        fig1 = px.line(df, x='Created At', y='Time', title='Session Time Over Time')
        fig1.update_layout(xaxis_title='Date', yaxis_title='Session Time (minutes)', xaxis=dict(tickangle=45))
        plots.append(fig1)

    if 'goal_distribution' in plot_names:
        fig2 = px.histogram(df, x='Goal', title='Goal Distribution')
        fig2.update_layout(xaxis_title='Goal', yaxis_title='Count', xaxis=dict(tickangle=45))
        plots.append(fig2)

    if 'session_duration_distribution' in plot_names:
        fig3 = px.histogram(df, x='Time', nbins=20, title='Session Duration Distribution')
        fig3.update_layout(xaxis_title='Session Duration (minutes)', yaxis_title='Frequency')
        plots.append(fig3)

    if 'elapsed_time_by_goal' in plot_names:
        fig4 = px.bar(df_filtered, x='Goal', y='Elapsed', title='Total Elapsed Time by Goal (Excluding 60-min Sessions)', 
                      labels={'Elapsed':'Total Elapsed Time (minutes)'})
        fig4.update_layout(xaxis=dict(tickangle=45))
        plots.append(fig4)

    if 'session_time_vs_elapsed' in plot_names:
        fig5 = px.scatter(df_filtered, x='Time', y='Elapsed', title='Session Time vs Elapsed Time (Excluding 60-min Sessions)')
        fig5.update_layout(xaxis_title='Session Time (minutes)', yaxis_title='Elapsed Time (minutes)')
        plots.append(fig5)

    if 'average_elapsed_time' in plot_names:
        fig6 = px.line(df_filtered, x='Created At', y='Elapsed', title='Average Elapsed Time per Session Over Time (Excluding 60-min Sessions)')
        fig6.update_layout(xaxis_title='Date', yaxis_title='Average Elapsed Time (minutes)', xaxis=dict(tickangle=45))
        plots.append(fig6)

    if 'sessions_over_time' in plot_names:
        sessions_over_time = df.groupby(df['Created At'].dt.date).size()
        fig7 = px.line(sessions_over_time, title='Number of Sessions Over Time')
        fig7.update_layout(xaxis_title='Date', yaxis_title='Number of Sessions', xaxis=dict(tickangle=45))
        plots.append(fig7)

    if 'total_elapsed_time_over_time' in plot_names:
        total_elapsed_over_time = df_filtered.groupby(df_filtered['Created At'].dt.date)['Elapsed'].sum()
        fig8 = px.line(total_elapsed_over_time, title='Total Elapsed Time Over Time (Excluding 60-min Sessions)')
        fig8.update_layout(xaxis_title='Date', yaxis_title='Total Elapsed Time (minutes)', xaxis=dict(tickangle=45))
        plots.append(fig8)

    # Convert plots to HTML for display
    plots_html = [plot.to_html(full_html=False) for plot in plots]

    return jsonify({
        'summary_stats': summary_stats,
        'plots': plots_html,
        'no_data': False
    })

@app.route('/generate_report', methods=['POST'])
def generate_report():
    df = read_csv(CSV_FILE_PATH)
    df = preprocess_data(df)
    df_filtered = filter_sessions(df)

    # Generate summary statistics
    summary_stats = {
        'total_sessions': len(df),
        'average_session_time': df['Time'].mean(),
        'median_session_time': df['Time'].median(),
        'total_elapsed_time': df['Elapsed'].sum(),
        'sessions_per_goal': df['Goal'].value_counts().to_dict()
    }

    # Generate plots
    plots = []
    plot_names = request.form.getlist('plot_options')

    if 'session_time_over_time' in plot_names:
        fig1 = px.line(df, x='Created At', y='Time', title='Session Time Over Time')
        fig1.update_layout(xaxis_title='Date', yaxis_title='Session Time (minutes)', xaxis=dict(tickangle=45))
        plots.append(fig1)

    if 'goal_distribution' in plot_names:
        fig2 = px.histogram(df, x='Goal', title='Goal Distribution')
        fig2.update_layout(xaxis_title='Goal', yaxis_title='Count', xaxis=dict(tickangle=45))
        plots.append(fig2)

    if 'session_duration_distribution' in plot_names:
        fig3 = px.histogram(df, x='Time', nbins=20, title='Session Duration Distribution')
        fig3.update_layout(xaxis_title='Session Duration (minutes)', yaxis_title='Frequency')
        plots.append(fig3)

    if 'elapsed_time_by_goal' in plot_names:
        fig4 = px.bar(df_filtered, x='Goal', y='Elapsed', title='Total Elapsed Time by Goal (Excluding 60-min Sessions)', 
                      labels={'Elapsed':'Total Elapsed Time (minutes)'})
        fig4.update_layout(xaxis=dict(tickangle=45))
        plots.append(fig4)

    if 'session_time_vs_elapsed' in plot_names:
        fig5 = px.scatter(df_filtered, x='Time', y='Elapsed', title='Session Time vs Elapsed Time (Excluding 60-min Sessions)')
        fig5.update_layout(xaxis_title='Session Time (minutes)', yaxis_title='Elapsed Time (minutes)')
        plots.append(fig5)

    if 'average_elapsed_time' in plot_names:
        fig6 = px.line(df_filtered, x='Created At', y='Elapsed', title='Average Elapsed Time per Session Over Time (Excluding 60-min Sessions)')
        fig6.update_layout(xaxis_title='Date', yaxis_title='Average Elapsed Time (minutes)', xaxis=dict(tickangle=45))
        plots.append(fig6)

    if 'sessions_over_time' in plot_names:
        sessions_over_time = df.groupby(df['Created At'].dt.date).size()
        fig7 = px.line(sessions_over_time, title='Number of Sessions Over Time')
        fig7.update_layout(xaxis_title='Date', yaxis_title='Number of Sessions', xaxis=dict(tickangle=45))
        plots.append(fig7)

    if 'total_elapsed_time_over_time' in plot_names:
        total_elapsed_over_time = df_filtered.groupby(df_filtered['Created At'].dt.date)['Elapsed'].sum()
        fig8 = px.line(total_elapsed_over_time, title='Total Elapsed Time Over Time (Excluding 60-min Sessions)')
        fig8.update_layout(xaxis_title='Date', yaxis_title='Total Elapsed Time (minutes)', xaxis=dict(tickangle=45))
        plots.append(fig8)

    pdf = create_pdf_report(plots, summary_stats)
    
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, attachment_filename='arcade_sessions_report.pdf', as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], CSV_FILE_PATH))
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
