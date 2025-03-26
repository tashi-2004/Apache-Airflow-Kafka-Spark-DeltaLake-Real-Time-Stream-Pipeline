import os
import json
import websocket
from kafka import KafkaProducer
import requests
import cbor2
from dotenv import load_dotenv

load_dotenv()
BSKY_USERNAME = os.getenv("ATP_EMAIL")
BSKY_PASSWORD = os.getenv("ATP_PASSWORD")

KAFKA_SERVER = "localhost:9092"
TOPIC = "bluesky_data"
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TARGET_DIDS = {
    "did:plc:u6mkbcgviwlbhuwqirmhcgu3": "elpais.com",
    "did:plc:humoyyfleayy76szpd5nqmw5": "catalannews.com"
}

def authenticate_bluesky():
    auth_url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    auth_data = {
        "identifier": BSKY_USERNAME,
        "password": BSKY_PASSWORD
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(auth_url, json=auth_data, headers=headers)
    if response.status_code == 200:
        auth_response = response.json()
        return auth_response["access_token"]
    else:
        print(f"Authentication failed: {response.status_code}")
        return None

def fetch_bluesky_data():
    """Subscribe to the Bluesky stream via WebSocket and send messages to Kafka."""
    access_token = authenticate_bluesky()
    if not access_token:
        print("Authentication failed, aborting data fetch.")
        return

    uri = "wss://bsky.social/xrpc/com.atproto.sync.subscribeRepos"

    def on_message(ws, message):
        """Handle incoming messages from the WebSocket."""
        print(f"Raw message received: {message}")
        try:
            message_data = cbor2.loads(message)
            print(f"Decoded message: {message_data}")
            producer.send(TOPIC, message_data)
            print(f"Message sent to Kafka: {message_data}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def on_error(ws, error):
        """Handle WebSocket errors."""
        print(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        """Handle WebSocket closure."""
        print("WebSocket connection closed.")

    def on_open(ws):
        """Notify when the WebSocket connection is established."""
        print("WebSocket connection established.")

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        uri,
        header={"Authorization": f"Bearer {access_token}"},
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    fetch_bluesky_data()
