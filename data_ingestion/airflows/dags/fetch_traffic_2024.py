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

def ingest_traffic_data_2024():
    data_path = '/home/tashi/BDM_Project/2024_12_Desembre_ITINERARIS_ITINERARIS.csv'
    df = pd.read_csv(data_path)
    print(df.head())

dag = DAG(
    'fetch_traffic_2024',
    description='Ingest Traffic Data for 2024',
    schedule_interval='@daily',  
    start_date=datetime(2024, 12, 1),
    catchup=False,
)

ingest_traffic_2024_task = PythonOperator(
    task_id='ingest_traffic_2024',
    python_callable=ingest_traffic_data_2024,
    dag=dag,
)

