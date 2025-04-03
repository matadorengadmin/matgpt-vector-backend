# command_runner.py

import os
import logging
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://matgpt-vector-backend-production.up.railway.app")

# ✅ FIXED: wrapped in "classes": []
schema = {
    "classes": [
        {
            "class": "SlackMessage",
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
    ]
}

@app.get("/")
def root():
    return {"status": "Command runner ready"}

@app.get("/run")
def run(task: str):
    if task == "create_schema":
        try:
            logging.info(f"🧠 Sending schema to {WEAVIATE_URL}/v1/schema")
            res = requests.post(f"{WEAVIATE_URL}/v1/schema", json=schema)
            res.raise_for_status()
            return {"status": "✅ Schema created", "response": res.json()}
        except Exception as e:
            logging.error(f"❌ Schema creation failed: {e}")
            return JSONResponse(status_code=500, content={"error": str(e)})
    return JSONResponse(status_code=404, content={"detail": "Not Found"})


