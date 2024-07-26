from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)

# Constants
CSV_FILE_PATH = 'arcade_sessions.csv'

def read_csv(file_path):
    return pd.read_csv(file_path, encoding='ISO-8859-1')

def preprocess_data(df):
    df['Created At'] = pd.to_datetime(df['Created At'])
    return df

def filter_sessions(df):
    return df[df['Time'] != 60]

@app.route('/', methods=['GET', 'POST'])
def index():
    df = read_csv(CSV_FILE_PATH)
    df = preprocess_data(df)
    df_filtered = filter_sessions(df)
    
    start_date = request.form.get('start_date', df['Created At'].min().strftime('%Y-%m-%d'))
    end_date = request.form.get('end_date', df['Created At'].max().strftime('%Y-%m-%d'))
    
    df = df[(df['Created At'] >= start_date) & (df['Created At'] <= end_date)]
    df_filtered = df_filtered[(df_filtered['Created At'] >= start_date) & (df_filtered['Created At'] <= end_date)]

    # Create visualizations
    plots = []

    # Session Time Over Time
    fig1 = px.line(df, x='Created At', y='Time', title='Session Time Over Time')
    fig1.update_layout(xaxis_title='Date', yaxis_title='Session Time (minutes)', xaxis=dict(tickangle=45))
    plots.append(fig1.to_html(full_html=False))

    # Goal Distribution
    fig2 = px.histogram(df, x='Goal', title='Goal Distribution')
    fig2.update_layout(xaxis_title='Goal', yaxis_title='Count', xaxis=dict(tickangle=45))
    plots.append(fig2.to_html(full_html=False))

    # Session Duration Distribution
    fig3 = px.histogram(df, x='Time', nbins=20, title='Session Duration Distribution')
    fig3.update_layout(xaxis_title='Session Duration (minutes)', yaxis_title='Frequency')
    plots.append(fig3.to_html(full_html=False))

    # Total Elapsed Time by Goal (Excluding 60-min Sessions)
    fig4 = px.bar(df_filtered, x='Goal', y='Elapsed', title='Total Elapsed Time by Goal (Excluding 60-min Sessions)', 
                  labels={'Elapsed':'Total Elapsed Time (minutes)'})
    fig4.update_layout(xaxis=dict(tickangle=45))
    plots.append(fig4.to_html(full_html=False))

    # Session Time vs Elapsed Time (Excluding 60-min Sessions)
    fig5 = px.scatter(df_filtered, x='Time', y='Elapsed', title='Session Time vs Elapsed Time (Excluding 60-min Sessions)')
    fig5.update_layout(xaxis_title='Session Time (minutes)', yaxis_title='Elapsed Time (minutes)')
    plots.append(fig5.to_html(full_html=False))

    # Cumulative Elapsed Time Over Time
    fig6 = px.line(df, x='Created At', y=df['Elapsed'].cumsum(), title='Cumulative Elapsed Time Over Time')
    fig6.update_layout(xaxis_title='Date', yaxis_title='Cumulative Elapsed Time (minutes)', xaxis=dict(tickangle=45))
    plots.append(fig6.to_html(full_html=False))

    # Session Count by Date
    df['Date'] = df['Created At'].dt.date
    fig7 = px.histogram(df, x='Date', title='Session Count by Date')
    fig7.update_layout(xaxis_title='Date', yaxis_title='Count', xaxis=dict(tickangle=45))
    plots.append(fig7.to_html(full_html=False))

    return render_template('index.html', plots=plots, start_date=start_date, end_date=end_date)

if __name__ == '__main__':
    app.run(debug=True)
