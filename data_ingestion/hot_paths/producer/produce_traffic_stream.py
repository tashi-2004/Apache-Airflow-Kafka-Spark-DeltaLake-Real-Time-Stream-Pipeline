from kafka import KafkaProducer
import json
import pandas as pd
from time import sleep

KAFKA_SERVER = "localhost:9092"
TOPIC = "traffic_data_2025"
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def read_traffic_data_from_csv():
    file_path = "/home/tashi/BDM_Project/2025_03_Marc_ITINERARIS_ITINERARIS.csv" 
    try:
        df = pd.read_csv(file_path)
        if 'idTram' in df.columns and 'tempsPrevist' in df.columns:
            print("Successfully read traffic data from CSV.")
            return df.to_dict(orient="records")  
        else:
            print("CSV file doesn't have the expected columns.")
            return []
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return []

def send_traffic_data():
    while True:
        traffic_data = read_traffic_data_from_csv()
        if traffic_data:
            for record in traffic_data:
                producer.send(TOPIC, value=record)
                print(f"Sent data: {record}")
        else:
            print("No data to send.")
        sleep(10) 

if __name__ == "__main__":
    send_traffic_data()

