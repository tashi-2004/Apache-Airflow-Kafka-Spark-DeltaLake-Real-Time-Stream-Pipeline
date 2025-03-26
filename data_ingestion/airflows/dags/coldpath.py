from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import subprocess

dag = DAG(
    'coldpath_ingestion',  
    description='Coldpath Data Ingestion DAG',
    schedule_interval='@daily',  
    start_date=datetime(2025, 3, 21), 
    catchup=False,  
)

def run_coldpath_script(script_name):
    subprocess.run(["python3", script_name], check=True)


ingest_google_maps_images = PythonOperator(
    task_id='ingest_cold_google_maps_images',
    python_callable=run_coldpath_script,
    op_args=["/home/tashi/BDM_Project/data_ingestion/cold_paths/ingest_cold_google_maps_images.py"],
    dag=dag,
)

ingest_serapi_images = PythonOperator(
    task_id='ingest_cold_serapi_images',
    python_callable=run_coldpath_script,
    op_args=["/home/tashi/BDM_Project/data_ingestion/cold_paths/ingest_cold_serapi_images.py"],  
    dag=dag,
)

ingest_traffic_data = PythonOperator(
    task_id='ingest_cold_traffic_data',
    python_callable=run_coldpath_script,
    op_args=["/home/tashi/BDM_Project/data_ingestion/cold_paths/ingest_cold_traffic_data.py"], 
    dag=dag,
)

ingest_twitter_data = PythonOperator(
    task_id='ingest_cold_twitter_data',
    python_callable=run_coldpath_script,
    op_args=["/home/tashi/BDM_Project/data_ingestion/cold_paths/ingest_cold_twitter_data.py"],
    dag=dag,
)

ingest_google_maps_images >> ingest_serapi_images >> ingest_traffic_data >> ingest_twitter_data

