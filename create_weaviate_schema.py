import requests

WEAVIATE_URL = "https://matgpt-vector-backend-production.up.railway.app"

schema = {
    "class": "SlackMessage",
    "description": "Messages exchanged in Slack with roles and metadata",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
            "vectorizeClassName": False
        }
    },
    "properties": [
        {"name": "message_id", "dataType": ["text"]},
        {"name": "user", "dataType": ["text"]},
        {"name": "timestamp", "dataType": ["text"]},
        {"name": "channel", "dataType": ["text"]},
        {"name": "text", "dataType": ["text"]},
        {"name": "role", "dataType": ["text"]},
        {"name": "thread_ts", "dataType": ["text"]}  # optional for threads
    ]
}

response = requests.post(
    f"{WEAVIATE_URL}/v1/schema",
    json=schema,
    headers={"Content-Type": "application/json"}
)

print("Status:", response.status_code)
print(response.text)
