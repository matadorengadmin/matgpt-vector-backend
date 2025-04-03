# chatgpt_agent.py
import os
import openai
import logging

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(history):
    logging.info("🎯 Sending prompt to OpenAI...")
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": msg["role"], "content": msg["content"]} for msg in history],
        )
        reply = response.choices[0].message.content
        logging.info("✅ OpenAI responded")
        return reply
    except Exception as e:
        logging.error(f"❌ OpenAI error: {e}")
        return "Sorry, something went wrong with my brain."
