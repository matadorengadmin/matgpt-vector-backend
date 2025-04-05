import os
import logging
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://matgpt-vector-backend-production.up.railway.app")

# ✅ Final schema — camelCase property names with OpenAI vectorization
schema = {
    "class": "SlackMessage",
    "description": "A message from Slack with metadata",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
            "vectorizeClassName": True
        }
    },
    "properties": [
        {
            "name": "messageId",
            "description": "Unique identifier for the Slack message",
            "dataType": ["text"],
            "indexFilterable": True
        },
        {
            "name": "user",
            "description": "User who sent the message",
            "dataType": ["text"],
            "indexFilterable": True
        },
        {
            "name": "timestamp",
            "description": "Time when message was sent",
            "dataType": ["text"],
            "indexFilterable": True
        },
        {
            "name": "channel",
            "description": "Slack channel of the message",
            "dataType": ["text"],
            "indexFilterable": True
        },
        {
            "name": "text",
            "description": "Actual message content",
            "dataType": ["text"],
            "indexFilterable": True
        },
        {
            "name": "role",
            "description": "Role of sender (user or assistant)",
            "dataType": ["text"],
            "indexFilterable": True
        },
        {
            "name": "threadTs",
            "description": "Slack thread timestamp, if part of a thread",
            "dataType": ["text"],
            "indexFilterable": True
        }
    ]
}

@app.get("/")
def root():
    return {"status": "Command runner ready"}

@app.get("/run")
def run(task: str):
    if task == "create_schema":
        try:
            logging.info(f"📤 Posting schema to {WEAVIATE_URL}/v1/schema")
            response = requests.post(f"{WEAVIATE_URL}/v1/schema", json=schema)
            response.raise_for_status()
            return {"status": "✅ Schema created", "response": response.json()}
        except Exception as e:
            logging.error(f"❌ Schema creation failed: {e}")
            return JSONResponse(status_code=500, content={"error": str(e)})
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

