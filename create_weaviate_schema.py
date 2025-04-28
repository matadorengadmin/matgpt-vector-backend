import requests

WEAVIATE_URL = "https://matgpt-vector-backend-production.up.railway.app"

# Define SlackMessage schema
slack_schema = {
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

# Define UpgradeLog schema
upgrade_log_schema = {
    "class": "UpgradeLog",
    "description": "Log of DevBot upgrade patches and attempts",
    "vectorizer": "none",
    "properties": [
        {"name": "app", "dataType": ["text"]},
        {"name": "threadTs", "dataType": ["text"]},
        {"name": "upgradeGoal", "dataType": ["text"]},
        {"name": "upgradeStatus", "dataType": ["text"]},
        {"name": "patchSummary", "dataType": ["text"]},
        {"name": "errorSummary", "dataType": ["text"]},
        {"name": "fileList", "dataType": ["text[]"]},
        {"name": "timestamp", "dataType": ["date"]}
    ]
}

# Define ThreadAssociation schema (optional but recommended)
thread_association_schema = {
    "class": "ThreadAssociation",
    "description": "Mapping between Slack thread_ts and OpenAI thread_id",
    "vectorizer": "none",
    "properties": [
        {"name": "threadTs", "dataType": ["text"]},
        {"name": "openAiThreadId", "dataType": ["text"]},
        {"name": "appName", "dataType": ["text"]},
        {"name": "filesInjected", "dataType": ["boolean"]},
        {"name": "timestamp", "dataType": ["date"]}
    ]
}

# Bundle all schemas
all_schemas = [slack_schema, upgrade_log_schema, thread_association_schema]

for schema in all_schemas:
    response = requests.post(
        f"{WEAVIATE_URL}/v1/schema",
        json=schema,
        headers={"Content-Type": "application/json"}
    )
    print(f"Created class {schema['class']}: Status {response.status_code}")
    print(response.text)
