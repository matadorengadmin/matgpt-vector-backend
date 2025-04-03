# slack_bot.py

import os
import logging
import requests

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")


def send_slack_message(channel: str, text: str):
    logging.info(f"📢 Sending message to Slack channel {channel}: {text}")
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        logging.error(f"Slack API error: {response.status_code} - {response.text}")
    else:
        logging.info(f"✅ Slack API response: {response.status_code} - {response.text}")


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
