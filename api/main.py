import requests
import csv
import os


SLACK_API_TOKEN = 
SLACK_USER_ID = 
CSV_FILE_PATH = 

headers = {
    'Authorization': f'Bearer {SLACK_API_TOKEN}'
}

def fetch_sessions():
    url = f'https://hackhour.hackclub.com/api/history/{SLACK_USER_ID}'
    response = requests.get(url, headers=headers)
