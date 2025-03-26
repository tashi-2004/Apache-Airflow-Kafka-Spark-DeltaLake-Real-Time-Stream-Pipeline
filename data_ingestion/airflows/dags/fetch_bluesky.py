import os
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("/home/tashi/airflow/env")  

ATP_EMAIL = os.getenv("ATP_EMAIL")
ATP_PASSWORD = os.getenv("ATP_PASSWORD")

def authenticate_bluesky():
    """Authenticate with BlueSky and return the access token."""
    auth_url = "https://bsky.social/xrpc/com.atproto.server.createSession"  
    auth_data = {
        "identifier": ATP_EMAIL,  
        "password": ATP_PASSWORD,  
    }

    response = requests.post(auth_url, json=auth_data)  
    
    if response.status_code == 200:
        try:
            auth_token = response.json().get("accessJwt")
            if auth_token:
                print("Authentication successful.")
                return auth_token
            else:
                print("Access token not found in the response.")
                return None
        except Exception as e:
            print(f"Error processing authentication response: {e}")
            return None
    else:
        print(f"Failed to authenticate. Status code: {response.status_code}")
        return None

def ingest_bluesky_data():
    """Ingest data from BlueSky."""
    token = authenticate_bluesky()

    if token is None:
        print("Authentication failed, aborting data fetch.")
        return

    url = "https://api.bsky.app/v1/posts"  
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Fetched Data: {data}")  
        except Exception as e:
            print(f"Error parsing data: {e}")
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")
        print(f"Response: {response.text}")

dag = DAG(
    'fetch_bluesky',
    description='Fetch BlueSky Data',
    schedule_interval='@hourly', 
    start_date=datetime(2025, 3, 21),
    catchup=False,
)


ingest_bluesky_task = PythonOperator(
    task_id='ingest_bluesky',
    python_callable=ingest_bluesky_data,
    dag=dag,
)

