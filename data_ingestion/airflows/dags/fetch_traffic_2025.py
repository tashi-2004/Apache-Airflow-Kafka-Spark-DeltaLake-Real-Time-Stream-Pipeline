import os
import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


ATP_EMAIL = os.getenv('ATP_EMAIL')
ATP_PASSWORD = os.getenv('ATP_PASSWORD')
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
API_GOOGLE_MAPS = os.getenv('API_GOOGLE_MAPS')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

def ingest_traffic_data_2025():
    data_path = '/home/tashi/BDM_Project/2025_03_Marc_ITINERARIS_ITINERARIS.csv'  
    df = pd.read_csv(data_path)
    print(df.head())

dag = DAG(
    'fetch_traffic_2025',
    description='Ingest Traffic Data for 2025',
    schedule_interval='@daily', 
    start_date=datetime(2025, 3, 21), 
    catchup=False, 
)


ingest_traffic_2025_task = PythonOperator(
    task_id='ingest_traffic_2025',
    python_callable=ingest_traffic_data_2025,
    dag=dag,
)


