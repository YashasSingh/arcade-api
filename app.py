from flask import Flask, render_template
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

@app.route('/')
def index():
    df = read_csv(CSV_FILE_PATH)
    df = preprocess_data(df)
    df_filtered = filter_sessions(df)
    
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

    # Average Elapsed Time per Session Over Time (Excluding 60-min Sessions)
    fig6 = px.line(df_filtered, x='Created At', y='Elapsed', title='Average Elapsed Time per Session Over Time (Excluding 60-min Sessions)')
    fig6.update_layout(xaxis_title='Date', yaxis_title='Average Elapsed Time (minutes)', xaxis=dict(tickangle=45))
    plots.append(fig6.to_html(full_html=False))

    # Number of Sessions Over Time
    sessions_over_time = df.groupby(df['Created At'].dt.date).size()
    fig7 = px.line(sessions_over_time, title='Number of Sessions Over Time')
    fig7.update_layout(xaxis_title='Date', yaxis_title='Number of Sessions', xaxis=dict(tickangle=45))
    plots.append(fig7.to_html(full_html=False))

    # Total Elapsed Time Over Time (Excluding 60-min Sessions)
    total_elapsed_over_time = df_filtered.groupby(df_filtered['Created At'].dt.date)['Elapsed'].sum()
    fig8 = px.line(total_elapsed_over_time, title='Total Elapsed Time Over Time (Excluding 60-min Sessions)')
    fig8.update_layout(xaxis_title='Date', yaxis_title='Total Elapsed Time (minutes)', xaxis=dict(tickangle=45))
    plots.append(fig8.to_html(full_html=False))

    return render_template('index.html', plots=plots)

if __name__ == '__main__':
    app.run(debug=True)
