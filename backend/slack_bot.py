import os
import requests
import logging
from backend.vector_store import add_slack_message

def send_slack_message(channel: str, text: str, user: str = None, timestamp: str = None, role: str = "assistant", original_text: str = None, client_msg_id: str = None):
    token = os.getenv("SLACK_BOT_TOKEN")

    logging.info(f"Using SLACK_BOT_TOKEN: {token[:12]}...")

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel": channel,
        "text": text
    }

    response = requests.post(url, headers=headers, json=payload)
    logging.info(f"Slack API response: {response.status_code} {response.text}")

    # Store the original message in Weaviate (if data is provided)
    if user and timestamp and original_text:
        message_id = client_msg_id or timestamp
        try:
            add_slack_message(
                message_id=message_id,
                user=user,
                timestamp=timestamp,
                channel=channel,
                text=original_text,
                role=role
            )
            logging.info(f"✅ Stored message in Weaviate: {message_id}")
        except Exception as e:
            logging.error(f"❌ Failed to store message in Weaviate: {e}")

    return response.json()
