import os
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from datetime import datetime
from PIL import Image
import pandas as pd

spark = SparkSession.builder \
    .appName("DataProcessing") \
    .config("spark.jars", "/home/tashi/spark/jars/delta-spark_2.13-3.3.0.jar") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:3.3.0") \
    .getOrCreate()

raw_data_path = "/home/tashi/BDM_Project/storage/delta/raw"
metadata_storage_path = "/home/tashi/BDM_Project/storage/delta/metadata"

social_media_data_path = os.path.join(raw_data_path, "social_media_data/bluesky/BlueSky")
traffic_2024_data_path = os.path.join(raw_data_path, "traffic_data/2024")
traffic_2025_data_path = os.path.join(raw_data_path, "traffic_data/2025")
serapi_data_path = os.path.join(raw_data_path, "images/serapi")
twitter_data_path = os.path.join(raw_data_path, "social_media_data/twitter")
google_maps_data_path = os.path.join(raw_data_path, "images/googlemaps")

def create_metadata(dataset_name, directory_path, file_extension, metadata_storage_path):
    files = os.listdir(directory_path)
    files = [file for file in files if file.endswith(file_extension)]
    
    if not files:
        print(f"No files with extension {file_extension} found in {directory_path}")
        return
    
    all_metadata = []
    
    for file in files:
        file_path = os.path.join(directory_path, file)
        
        if file_extension == ".csv":
            df = pd.read_csv(file_path)
            num_rows = len(df)
            num_columns = len(df.columns)
            column_names = df.columns.tolist()
            column_data_types = df.dtypes.astype(str).tolist()
            file_size = os.path.getsize(file_path)  
            sample_rows = df.head(5).to_dict(orient="records") 
            
            file_metadata = {
                "file_name": file,
                "file_size_in_bytes": file_size,
                "sample_data": sample_rows,
                "timestamp": datetime.now().isoformat()
            }
        
        elif file_extension == ".json":
            with open(file_path, "r") as f:
                data = json.load(f)
            
            file_size = os.path.getsize(file_path)  
            sample_data = data if isinstance(data, dict) else data[:5]  
            file_metadata = {
                "file_name": file,
                "file_size_in_bytes": file_size,
                "sample_data": sample_data,
                "timestamp": datetime.now().isoformat()
            }
        
        elif file_extension == ".jpg":
            img = Image.open(file_path)
            image_width, image_height = img.size
            image_file_size = os.path.getsize(file_path) / 1024  
            
            file_metadata = {
                "file_name": file,
                "file_size_in_bytes": image_file_size,
                "image_dimensions": f"{image_width}x{image_height}",
                "timestamp": datetime.now().isoformat()
            }
        
        all_metadata.append(file_metadata)
    
    metadata = {
        "dataset_name": dataset_name,
        "data_count": len(files), 
        "files_metadata": all_metadata,  
        "timestamp": datetime.now().isoformat()
    }
    
    metadata_file_path = f"{metadata_storage_path}/{dataset_name}_metadata.json"
    with open(metadata_file_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    print(f"Metadata saved: {metadata_file_path}")

def load_raw_data(file_path):
    return spark.read.json(file_path) 

def transform_data(raw_df):
    return raw_df.withColumn("ingestion_time", lit(datetime.now()))

def store_in_delta(df, delta_path):
    df.write.format("delta").mode("overwrite").save(delta_path)

def process_bluesky_data():
    raw_df = load_raw_data(social_media_data_path)
    transformed_df = transform_data(raw_df)
    
    print("Storing BlueSky Data to Delta Lake")
    store_in_delta(transformed_df, "/home/tashi/BDM_Project/storage/delta/social_media_data/delta")
    
    data_count = transformed_df.count()
    create_metadata("bluesky_data", social_media_data_path, ".json", metadata_storage_path)
    print("BlueSky data processing completed.")

def process_traffic_2024_data():
    raw_df = load_raw_data(traffic_2024_data_path)
    transformed_df = transform_data(raw_df)
    
    print("Storing 2024 Traffic data to Delta Lake")
    store_in_delta(transformed_df, "/home/tashi/BDM_Project/storage/delta/traffic_data/2024/delta")
    
    data_count = transformed_df.count()
    create_metadata("traffic_2024_data", traffic_2024_data_path, ".csv", metadata_storage_path)
    print("Traffic 2024 data processing completed.")

def process_traffic_2025_data():
    raw_df = load_raw_data(traffic_2025_data_path)
    transformed_df = transform_data(raw_df)
    
    print("Storing 2025 Traffic data to Delta Lake")
    store_in_delta(transformed_df, "/home/tashi/BDM_Project/storage/delta/traffic_data/2025/delta")
    
    data_count = transformed_df.count()
    create_metadata("traffic_2025_data", traffic_2025_data_path, ".json", metadata_storage_path)
    print("Traffic 2025 data processing completed.")

def process_serapi_data():
    raw_df = load_raw_data(serapi_data_path)
    transformed_df = transform_data(raw_df)
    
    print("Storing Serapi data to Delta Lake")
    store_in_delta(transformed_df, "/home/tashi/BDM_Project/storage/delta/serapi_data/delta")
    
    data_count = transformed_df.count()
    create_metadata("serapi_data", serapi_data_path, ".jpg", metadata_storage_path)
    print("Serapi data processing completed.")

def process_twitter_data():
    raw_df = load_raw_data(twitter_data_path)
    transformed_df = transform_data(raw_df)
    
    print("Storing Twitter data to Delta Lake")
    store_in_delta(transformed_df, "/home/tashi/BDM_Project/storage/delta/twitter_data/delta")
    
    data_count = transformed_df.count()
    create_metadata("twitter_data", twitter_data_path, ".csv", metadata_storage_path)
    print("Twitter data processing completed.")

def process_google_maps_data():
    raw_df = load_raw_data(google_maps_data_path)
    transformed_df = transform_data(raw_df)
    
    print("Storing Google Maps data to Delta Lake")
    store_in_delta(transformed_df, "/home/tashi/BDM_Project/storage/delta/google_maps_data/delta")
    
    data_count = transformed_df.count()
    create_metadata("google_maps_data", google_maps_data_path, ".jpg", metadata_storage_path)
    print("Google Maps data processing completed.")

if __name__ == "__main__":
    print("\t\t\t\t\t___________________________________________________")
    print("\t\t\t\t\t| Delta Lake Data Ingestion and Metadata Creation |")
    print("\t\t\t\t\t|_________________________________________________|")
    print("\n")
    process_bluesky_data()
    process_traffic_2024_data()
    process_traffic_2025_data()
    process_serapi_data()
    process_twitter_data()
    process_google_maps_data()
    print("Delta Lake ingestion and metadata creation complete :)")