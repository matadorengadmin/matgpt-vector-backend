import os
import requests
import hashlib
from pathlib import Path
from datetime import datetime
import json

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://matgpt-vector-backend-production.up.railway.app")
GITHUB_REPO_PATH = os.getenv("SHADOW_REPO", "matgpt-devbot-shadow")  

def sha256_of_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def upload_file_to_weaviate(filepath: Path):
    relative_path = filepath.relative_to(GITHUB_REPO_PATH)
    filename = str(relative_path)
    content = filepath.read_text(errors="ignore")
    commit_hash = "initial-import"  # Later we can make this dynamic
    now = datetime.utcnow().isoformat()

    object_id = sha256_of_text(filename)

    payload = {
        "class": "CodeFile",
        "id": object_id,
        "properties": {
            "filename": filename,
            "content": content,
            "commitHash": commit_hash,
            "lastUpdated": now
        }
    }

    response = requests.post(f"{WEAVIATE_URL}/v1/objects", json=payload)
    if response.status_code not in (200, 201):
        print(f"❌ Failed to upload {filename}: {response.status_code} {response.text}")
    else:
        print(f"✅ Uploaded {filename}")

def sync_repo_to_weaviate():
    base_path = Path(GITHUB_REPO_PATH)
    if not base_path.exists():
        print(f"❌ Error: Repo path '{GITHUB_REPO_PATH}' does not exist.")
        return

    all_files = [f for f in base_path.rglob("*") if f.is_file()]
    print(f"📂 Found {len(all_files)} files to sync.")

    for file in all_files:
        upload_file_to_weaviate(file)

if __name__ == "__main__":
    sync_repo_to_weaviate()
