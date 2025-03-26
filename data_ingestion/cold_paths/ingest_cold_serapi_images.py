import os
import requests
import json
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))


LANDING_ZONE_RAW = os.path.join(BASE_DIR, "storage", "delta","raw", "images", "serapi")

os.makedirs(LANDING_ZONE_RAW, exist_ok=True)

def fetch_google_maps_images(query):
    params = {
        "q": query,
        "tbm": "isch", 
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("images_results", [])

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image saved: {save_path}")
        else:
            print(f"Failed to download image: {image_url}")
    except Exception as e:
        print(f"Error downloading image: {e}")

def save_images():
    query = "Barcelona traffic"
    images = fetch_google_maps_images(query)

    for idx, image in enumerate(images):
        image_url = image["thumbnail"]
        image_filename = f"google_maps_image_{idx}.jpg"
        image_path = os.path.join(LANDING_ZONE_RAW, image_filename)

        download_image(image_url, image_path)


if __name__ == "__main__":
    print("\t\t\t\t\t______________________")
    print("\t\t\t\t\t| Cold Serapi Images |")
    print("\t\t\t\t\t|____________________|")
    print("\n")
    save_images()
