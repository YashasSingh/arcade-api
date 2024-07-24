import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
CSV_FILE_PATH = 'arcade_sessions.csv'

def read_csv(file_path):
    return pd.read_csv(file_path, encoding='ISO-8859-1')

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

def plot_goal_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Goal', order=df['Goal'].value_counts().index)
    plt.title('Goal Distribution')
    plt.xlabel('Goal')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_session_duration_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Time'], bins=20, kde=True)
    plt.title('Session Duration Distribution')
    plt.xlabel('Session Duration (minutes)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def plot_elapsed_time_vs_goal(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Goal', y='Elapsed', ci=None, estimator=sum, order=df['Goal'].value_counts().index)
    plt.title('Total Elapsed Time by Goal')
    plt.xlabel('Goal')
    plt.ylabel('Total Elapsed Time (minutes)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_sessions_per_day(df):
    plt.figure(figsize=(10, 6))
    df['Date'] = df['Created At'].dt.date
    sns.countplot(data=df, x='Date', order=df['Date'].value_counts().index)
    plt.title('Sessions Per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Sessions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    df = read_csv(CSV_FILE_PATH)
    df = preprocess_data(df)
    print(df.describe())
    plot_session_times(df)
    plot_goal_distribution(df)
    plot_session_duration_distribution(df)
    plot_elapsed_time_vs_goal(df)
    plot_sessions_per_day(df)

if __name__ == '__main__':
    main()
