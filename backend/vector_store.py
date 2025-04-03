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

    logging.info(f"🔁 Sending to Weaviate at {WEAVIATE_URL}/v1/objects")
    logging.info(f"📦 Payload: {payload}")

    try:
        response = requests.post(f"{WEAVIATE_URL}/v1/objects", json=payload)
        response.raise_for_status()
        logging.info(f"✅ Weaviate response: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"❌ Weaviate store error: {e}")
        logging.error(f"❌ Full response (if available): {getattr(response, 'text', 'No response')}")

# 🔧 This is the name your app expects:
def add_slack_message(message_id, user, timestamp, channel, text, role):
    logging.info(f"🧠 add_slack_message called for: {role} - {text[:30]}")
    store_message_in_weaviate(message_id, user, timestamp, channel, text, role)
