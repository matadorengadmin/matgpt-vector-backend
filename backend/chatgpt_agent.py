import openai
import logging

def ask_openai(messages):
    logging.info("Preparing request for OpenAI")
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        raise
