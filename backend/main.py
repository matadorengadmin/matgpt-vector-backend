# backend/main.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.vector_store import add_slack_message

load_dotenv()

app = FastAPI()

class SlackMessage(BaseModel):
    message_id: str
    user: str
    timestamp: str
    channel: str
    text: str
    role: str

@app.get("/")
def root():
    return {"message": "Weaviate Vector Backend is running."}

@app.post("/test-insert")
def test_insert(message: SlackMessage):
    add_slack_message(message.dict())
    return {"status": "✅ Message inserted into Weaviate"}
