import os
import requests
import pandas as pd
from datetime import datetime

TRAFFIC_API_URL = "https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search?resource_id=57968ea7-f7da-43ce-ae8b-54fd8dd30b5f&limit=5"
SAVE_DIR = "/home/tashi/BDM_Project/storage/delta/raw/traffic_data/2024"

os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_traffic_data():
    try:
        response = requests.get(TRAFFIC_API_URL)
        if response.status_code == 200:
            print("Traffic data fetched.")
            print("\n")
            return response.json()  
        else:
            raise Exception(f"Failed to fetch traffic data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def process_traffic_data():
    data = fetch_traffic_data()
    if data:
        if 'result' in data and 'records' in data['result']:
            df = pd.DataFrame(data['result']['records'])
            filename = f"traffic_data_2024_{datetime.now().strftime('%Y%m%d')}.parquet"  
            file_path = os.path.join(SAVE_DIR, filename)  
            df.to_parquet(file_path, index=False)
            print(f"Data saved to {file_path}")
        else:
            print("No traffic data found.")
    else:
        print("Failed to process.")

if __name__ == "__main__":
    print("\t\t\t\t\t_____________________")
    print("\t\t\t\t\t| Cold Traffic Data |")
    print("\t\t\t\t\t|___________________|")
    print("\n")
    process_traffic_data()
