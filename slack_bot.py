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
