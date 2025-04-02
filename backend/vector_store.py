# backend/vector_store.py

import os
import requests
import logging

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://matgpt-vector-backend-production.up.railway.app")

def store_message_in_weaviate(message_id, user, timestamp, channel, text, role):
    payload = {
        "class": "SlackMessage",
        "properties": {
            "message_id": message_id,
            "user": user,
            "timestamp": timestamp,
            "channel": channel,
            "text": text,
            "role": role
        }
    }

    try:
        response = requests.post(f"{WEAVIATE_URL}/v1/objects", json=payload)
        response.raise_for_status()
        logging.info(f"Weaviate store success: {response.status_code}")
    except Exception as e:
        logging.error(f"Weaviate store error: {e}")
