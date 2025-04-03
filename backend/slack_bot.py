import os
import requests
import logging

def send_slack_message(channel: str, text: str):
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
    return response.json()
