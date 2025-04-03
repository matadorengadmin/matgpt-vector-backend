import os
import json
import logging
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

# === ENVIRONMENT ===
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://matgpt-vector-backend-production.up.railway.app")

# === APP SETUP ===
logging.basicConfig(level=logging.INFO)
app = FastAPI()

# === ROUTES ===
@app.get("/")
def root():
    return {"status": "MatGPT Devbot is live"}

@app.post("/slack/events")
async def slack_events(request: Request):
    body = await request.json()
    logging.info(f"Incoming Slack event body: {body}")

    if body.get("type") == "url_verification":
        return JSONResponse(content={"challenge": body["challenge"]})

    event = body.get("event", {})
    if event.get("type") == "app_mention":
        user = event["user"]
        text = event["text"]
        channel = event["channel"]
        timestamp = event["ts"]
        message_id = body.get("event_id", "unknown")

        logging.info(f"User {user} mentioned the bot in {channel} saying: {text}")

        # Load conversation history
        history = load_history()
        history.append({"role": "user", "content": text})
        history = history[-10:]

        try:
            reply = ask_openai(history)
            history.append({"role": "assistant", "content": reply})
            save_history(history)

            log_to_weaviate(message_id, user, timestamp, channel, text, "user")
            log_to_weaviate(message_id + "_response", "matgpt-devbot", timestamp, channel, reply, "assistant")

        except Exception as e:
            logging.error(f"OpenAI error: {e}")
            reply = "Sorry, I had trouble thinking just now. Try again in a sec?"

        send_slack_message(channel, reply)
        return JSONResponse(content={"ok": True})

    return JSONResponse(content={"ok": True})

# === HISTORY ===
def load_history():
    try:
        if os.path.exists("conversation_history.json"):
            with open("conversation_history.json", "r") as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load history: {e}")
    return []

def save_history(history):
    try:
        with open("conversation_history.json", "w") as f:
            json.dump(history, f)
    except Exception as e:
        logging.error(f"Failed to save history: {e}")

# === OPENAI ===
def ask_openai(history):
    logging.info("🧠 Preparing request for OpenAI")
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": history
    }
    response = httpx.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

# === SLACK ===
def send_slack_message(channel: str, text: str):
    logging.info(f"📢 Sending reply to Slack: {text}")
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
    logging.info(f"Slack API response: {response.status_code} {response.text}")

# === WEAVIATE ===
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
