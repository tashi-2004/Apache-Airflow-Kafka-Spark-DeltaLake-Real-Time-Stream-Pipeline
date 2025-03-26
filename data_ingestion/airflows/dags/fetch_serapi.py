import os
import requests
from dotenv import load_dotenv
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
load_dotenv("/home/tashi/airflow/env")
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
def fetch_serapi_traffic_images():
    url = "https://serpapi.com/google-maps-photos-api"  
    params = {
        'api_key': SERPAPI_KEY,  
        'type': 'traffic', 
        'location': '41.3870,2.1701',  
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data:
                print("Warning: The response is empty.")
            else:
                print("Data fetched successfully:", data)
                images = data.get('images', [])
                if images:
                    for idx, image_url in enumerate(images):
                        image_data = requests.get(image_url).content
                        output_dir = "/home/tashi/BDM_Project/landing_zone/google_maps_images"
                        os.makedirs(output_dir, exist_ok=True)  
                        output_file = os.path.join(output_dir, f"google_maps_image_{idx}.jpg")
                        with open(output_file, "wb") as f:
                            f.write(image_data)
                        print(f"Saved image: {output_file}")
                else:
                    print("No traffic images found in the response.")
        else:
            print(f"Error: Received status code {response.status_code}. Response: {response.text}")
    except Exception as e:
        print(f"Error occurred: {e}")

dag = DAG(
    'fetch_serapi_traffic_images',
    description='Fetch Traffic Images from SerpAPI',
    schedule_interval='@hourly',  
    start_date=datetime(2025, 3, 21),
    catchup=False,
)

fetch_serapi_task = PythonOperator(
    task_id='fetch_serapi_traffic_images_task',
    python_callable=fetch_serapi_traffic_images,
    dag=dag,
)

