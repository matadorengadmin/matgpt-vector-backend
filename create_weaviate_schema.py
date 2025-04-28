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

# Define CodeFile schema
codefile_schema = {
    "class": "CodeFile",
    "description": "Stores code files from the Shadow DevBot repo",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
            "vectorizeClassName": True
        }
    },
    "properties": [
        {
            "name": "filename",
            "dataType": ["text"],
            "description": "The relative path of the file, like backend/main.py",
            "moduleConfig": {
                "text2vec-openai": {"skip": False}
            }
        },
        {
            "name": "content",
            "dataType": ["text"],
            "description": "The full content of the file",
            "moduleConfig": {
                "text2vec-openai": {"skip": False}
            }
        },
        {
            "name": "commitHash",
            "dataType": ["text"],
            "description": "The git commit hash when this version was saved",
            "moduleConfig": {
                "text2vec-openai": {"skip": True}
            }
        },
        {
            "name": "lastUpdated",
            "dataType": ["date"],
            "description": "Timestamp when this file version was saved",
            "moduleConfig": {
                "text2vec-openai": {"skip": True}
            }
        }
    ]
}

# Define ShadowFile schema
shadow_file_schema = {
    "class": "ShadowFile",
    "description": "Stores upgraded files from the Shadow DevBot repo",
    "vectorizer": "none",
    "properties": [
        {
            "name": "fileName",
            "dataType": ["text"],
            "description": "The filename (e.g., main.py)",
        },
        {
            "name": "content",
            "dataType": ["text"],
            "description": "The full content of the file",
        },
        {
            "name": "appName",
            "dataType": ["text"],
            "description": "The app name this file belongs to (e.g., __shadow__)",
        }
    ]
}



# Bundle all schemas
all_schemas = [
    slack_schema,
    upgrade_log_schema,
    thread_association_schema,
    codefile_schema,
    shadow_file_schema,  # <-- add here
]


for schema in all_schemas:
    response = requests.post(
        f"{WEAVIATE_URL}/v1/schema",
        json=schema,
        headers={"Content-Type": "application/json"}
    )
    print(f"Created class {schema['class']}: Status {response.status_code}")
    print(response.text)
