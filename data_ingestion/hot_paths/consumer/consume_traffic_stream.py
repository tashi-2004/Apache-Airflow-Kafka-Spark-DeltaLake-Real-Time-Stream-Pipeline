from kafka import KafkaConsumer
import os
import pandas as pd
from datetime import datetime

KAFKA_SERVER = "localhost:9092"
TOPIC = "traffic_data_2025"
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    group_id="traffic-consumer-group"
)

SAVE_DIR = "/home/tashi/BDM_Project/storage/delta/raw/traffic_data/2025"
os.makedirs(SAVE_DIR, exist_ok=True)

def consume_traffic_data():
    for message in consumer:
        print(f"Received message: {message.value}")
        save_traffic_data(message.value)

def save_traffic_data(data):
    # Convert the data into a pandas DataFrame
    df = pd.DataFrame([data])  # Ensure the data is in a list format for DataFrame creation
    filename = f"traffic_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.parquet"
    file_path = os.path.join(SAVE_DIR, filename)

    # Save the DataFrame as a Parquet file
    df.to_parquet(file_path, engine='pyarrow')  # or 'fastparquet'
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    consume_traffic_data()

