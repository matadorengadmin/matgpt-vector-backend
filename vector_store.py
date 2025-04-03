# vector_store.py

import os
import logging
import requests

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://matgpt-vector-backend-production.up.railway.app")


def log_to_weaviate(message_id, user, timestamp, channel, text, role):
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
    logging.info(f"📤 Sending to Weaviate: {WEAVIATE_URL}/v1/objects")
    logging.info(f"📦 Payload: {payload}")
    try:
        response = requests.post(f"{WEAVIATE_URL}/v1/objects", json=payload)
        response.raise_for_status()
        logging.info(f"✅ Stored in Weaviate: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"❌ Weaviate store error: {e}")
        logging.error(f"❌ Full response (if available): {getattr(response, 'text', 'No response')}")

