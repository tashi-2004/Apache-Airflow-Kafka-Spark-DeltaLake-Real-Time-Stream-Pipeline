import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("/home/tashi/airflow/env")
GOOGLE_MAPS_API_KEY = os.getenv("API_GOOGLE_MAPS")

SAVE_DIR = os.path.join(os.path.expanduser("~"), "BDM_Project", "storage", "delta", "raw", "images", "googlemaps")
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_google_maps_images():
    if GOOGLE_MAPS_API_KEY is None:
        print("API key not found.")
        return

    url = "https://maps.googleapis.com/maps/api/staticmap?"
    params = {
        "size": "600x300", 
        "location": "40.714224,-73.961452",
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            filename = f"google_maps_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            file_path = os.path.join(SAVE_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(response.content)

            print("\t\t\t\t\t____________________________")
            print("\t\t\t\t\t| Cold Google Maps Images |")
            print("\t\t\t\t\t|__________________________|")
            print("\n")
            print(f"Google Maps image saved at: {file_path}")
            print("\n")

        else:
            print(f"Failed to fetch Google Maps image. Status Code: {response.status_code}")
            print(f"Response content: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_google_maps_images()
