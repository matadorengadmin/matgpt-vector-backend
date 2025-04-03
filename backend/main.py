# backend/main.py
import os
import json
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.chatgpt_agent import ask_openai
from backend.slack_bot import send_slack_message
from backend.vector_store import add_slack_message

logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.get("/")
async def root():
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
        history_path = "conversation_history.json"
        history = []
        if os.path.exists(history_path):
            try:
                with open(history_path, "r") as f:
                    history = json.load(f)
            except Exception as e:
                logging.error(f"Failed to load history: {e}")

        history.append({"role": "user", "content": text})
        history = history[-10:]

        try:
            reply = ask_openai(history)
            history.append({"role": "assistant", "content": reply})

            with open(history_path, "w") as f:
                json.dump(history, f)

            # Save to Weaviate
            logging.info("📦 Logging user message to Weaviate")
            add_slack_message(
                message_id=message_id,
                user=user,
                timestamp=timestamp,
                channel=channel,
                text=text,
                role="user"
            )

            logging.info("📦 Logging assistant response to Weaviate")
            add_slack_message(
                message_id=message_id + "_response",
                user="matgpt-devbot",
                timestamp=timestamp,
                channel=channel,
                text=reply,
                role="assistant"
            )

        except Exception as e:
            logging.error(f"OpenAI error: {e}")
            reply = "Sorry, I had trouble thinking just now. Try again in a sec?"

        send_slack_message(channel, reply)
        return JSONResponse(content={"ok": True})

    return JSONResponse(content={"ok": True"})
