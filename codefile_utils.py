import os
import requests

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://matgpt-vector-backend-production.up.railway.app")

def fetch_codefile_by_filename(filename: str):
    query = {
        "query": f"""
        {{
          Get {{
            CodeFile(where: {{
              path: ["filename"],
              operator: Equal,
              valueString: "{filename}"
            }}) {{
              filename
              content
              commitHash
              lastUpdated
            }}
          }}
        }}
        """
    }

    try:
        response = requests.post(f"{WEAVIATE_URL}/v1/graphql", json=query)
        if response.status_code != 200:
            print(f"❌ Failed to query Weaviate: {response.status_code} {response.text}")
            return None

        result = response.json()
        files = result.get("data", {}).get("Get", {}).get("CodeFile", [])
        if not files:
            print(f"⚠️ No file found with filename: {filename}")
            return None

        # We expect only one match
        return files[0]

    except Exception as e:
        print(f"❌ Exception during fetch: {e}")
        return None
