from backend.vector_store import add_slack_message

# Example test Slack message
test_message = {
    "message_id": "test-001",
    "user": "U12345678",
    "timestamp": "2025-04-02T14:00:00Z",
    "channel": "C12345678",
    "text": "This is a test Slack message for Weaviate vector store.",
    "role": "user"
}

add_slack_message(test_message)
print("✅ Test message inserted.")
