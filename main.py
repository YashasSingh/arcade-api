import requests
import csv
import os
import configparser
from datetime import datetime

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Fetch API token and user ID from configuration file
SLACK_API_TOKEN = config['slack']['api_token']
SLACK_USER_ID = config['slack']['user_id']
CSV_FILE_PATH = 'arcade_sessions.csv'

headers = {
    'Authorization': f'Bearer {SLACK_API_TOKEN}'
}

def fetch_sessions():
    url = f'https://hackhour.hackclub.com/api/history/{SLACK_USER_ID}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Failed to fetch sessions: {response.status_code}")
        return []

def write_to_csv(sessions):
    # Sort sessions by createdAt in ascending order
    sessions.sort(key=lambda x: datetime.fromisoformat(x['createdAt'].replace('Z', '+00:00')))
    
    with open(CSV_FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Created At', 'Time', 'Elapsed', 'Goal', 'Ended', 'Work'])
        for session in sessions:
            writer.writerow([
                session.get('createdAt', ''),
                session.get('time', ''),
                session.get('elapsed', ''),
                session.get('goal', ''),
                session.get('ended', ''),
                session.get('work', '')
            ])

def main():
    sessions = fetch_sessions()
    write_to_csv(sessions)
    print(f"Session data has been written to {CSV_FILE_PATH}")

if __name__ == '__main__':
    main()
