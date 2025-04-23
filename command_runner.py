import os
import logging
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://matgpt-vector-backend-production.up.railway.app")

# ✅ FIXED: CamelCase + valid OpenAI vectorizer schema
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
            "dataType": ["text"]
        },
        {
            "name": "user",
            "description": "User who sent the message",
            "dataType": ["text"]
        },
        {
            "name": "timestamp",
            "description": "Time when message was sent",
            "dataType": ["text"]
        },
        {
            "name": "channel",
            "description": "Slack channel of the message",
            "dataType": ["text"]
        },
        {
            "name": "text",
            "description": "Actual message content",
            "dataType": ["text"]
        },
        {
            "name": "role",
            "description": "Role of sender (user or assistant)",
            "dataType": ["text"]
        },
        {
            "name": "threadTs",
            "description": "Thread timestamp for Slack threads",
            "dataType": ["text"]
        },
        {
            "name": "tags",
            "description": "Tags for categorizing messages or uploaded content",
            "dataType": ["text[]"]
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
            response = requests.post(f"{WEAVIATE_URL}/v1/schema", json={"classes": [schema]})
            if response.status_code == 200:
                logging.info("✅ Schema created successfully.")
                return {"status": "✅ Schema created", "response": response.json()}
            else:
                # Log full response from Weaviate
                logging.error(f"❌ Schema creation failed.\nStatus: {response.status_code}\nResponse: {response.text}")
                return JSONResponse(status_code=500, content={
                    "status": "error",
                    "status_code": response.status_code,
                    "response": response.text
                })
        except Exception as e:
            logging.exception("❌ Exception during schema creation")
            return JSONResponse(status_code=500, content={"error": str(e)})

    return JSONResponse(status_code=404, content={"detail": "Not Found"})




