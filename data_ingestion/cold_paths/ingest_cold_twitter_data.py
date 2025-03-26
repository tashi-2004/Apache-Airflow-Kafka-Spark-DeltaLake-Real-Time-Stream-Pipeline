import os
import requests
import pandas as pd
from datetime import datetime
import time 

TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAN%2FhzwEAAAAAG3ATdlame3omTSnIQMVDgT%2FfXDo%3DDMwmTKUccrCojxBMP584lidrDgsu9fPO9uMUfQQNfpxZTgJIll" 
SAVE_DIR = "/home/tashi/BDM_Project/storage/delta/raw/social_media_data/twitter"

os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_twitter_data():
    if TWITTER_BEARER_TOKEN is None:
        print("Bearer token not found.")
        return

    url = "https://api.twitter.com/2/tweets/search/recent"  
    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
    }
    params = {
        "query": "from:transit", 
        "max_results": 10       
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            print("Twitter data Fetched.")
            print("\n")
            return response.json()  
        
        elif response.status_code == 429:
            reset_time = int(response.headers.get('x-rate-limit-reset', time.time()))
            sleep_time = reset_time - time.time() + 5  
            print(f"Rate limit reached. Retrying after {sleep_time} seconds...")
            time.sleep(sleep_time)
            return fetch_twitter_data()  
        else:
            raise Exception(f"Failed to fetch Twitter data: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def process_twitter_data():
    data = fetch_twitter_data()

    if data:
        if 'data' in data:
            df = pd.DataFrame(data['data'])  
            filename = f"twitter_data_{datetime.now().strftime('%Y%m%d')}.parquet" 
            file_path = os.path.join(SAVE_DIR, filename)  
            df.to_parquet(file_path, index=False) 
            print(f"Twitter data saved to {file_path}")
        else:
            print("No data found in the response.")
    else:
        print("Failed to process Twitter data.")

if __name__ == "__main__":
    print("\t\t\t\t\t_____________________")
    print("\t\t\t\t\t| Cold Twitter Data |")
    print("\t\t\t\t\t|___________________|")
    print("\n")
    process_twitter_data()

