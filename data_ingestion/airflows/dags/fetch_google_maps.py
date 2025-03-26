import os
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("/home/tashi/airflow/env") 
API_GOOGLE_MAPS = os.getenv("API_GOOGLE_MAPS")

def fetch_google_maps_data():
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = "restaurants in New York"  
    params = {
        'query': query,
        'key': API_GOOGLE_MAPS,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"Fetched Data: {data}")  

    else:
        print(f"Failed to fetch data, status code: {response.status_code}")
        print(f"Response: {response.text}")

dag = DAG(
    'fetch_google_maps',
    description='Fetch Google Maps Data',
    schedule_interval='@daily',
    start_date=datetime(2025, 3, 21),
    catchup=False,
)

fetch_google_maps_task = PythonOperator(
    task_id='fetch_google_maps_data_task',
    python_callable=fetch_google_maps_data,
    dag=dag,
)

