# backend/create_schema.py
import requests

def main():
    WEAVIATE_URL = "https://matgpt-vector-backend-production.up.railway.app"
    schema_payload = {
        "class": "SlackMessage",
        "description": "A Slack message stored for context and recall.",
        "vectorizer": "text2vec-openai",
        "properties": [
            {"name": "message_id", "dataType": ["string"]},
            {"name": "user", "dataType": ["string"]},
            {"name": "timestamp", "dataType": ["string"]},
            {"name": "channel", "dataType": ["string"]},
            {"name": "text", "dataType": ["text"]},
            {"name": "role", "dataType": ["string"]}
        ]
    }

    response = requests.post(f"{WEAVIATE_URL}/v1/schema", json=schema_payload)
    print("Schema creation status:", response.status_code)
    print("Response:", response.text)
