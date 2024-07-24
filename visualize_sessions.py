import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
CSV_FILE_PATH = 'arcade_sessions.csv'

def read_csv(file_path):
    return pd.read_csv(file_path)

def preprocess_data(df):
    # Convert 'Created At' to datetime
    df['Created At'] = pd.to_datetime(df['Created At'])
    return df

def plot_session_times(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Created At', y='Time', data=df, marker='o')
    plt.title('Session Time Over Time')
    plt.xlabel('Date')
    plt.ylabel('Session Time (minutes)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()