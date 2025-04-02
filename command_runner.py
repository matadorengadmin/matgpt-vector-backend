# command_runner.py
from fastapi import FastAPI, Query
from backend import create_schema
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Command runner ready"}

@app.get("/run")
def run_command(task: str = Query(...)):
    if task == "create_schema":
        try:
            create_schema.main()  # run schema creation
            return {"status": "✅ Schema created"}
        except Exception as e:
            return {"status": "❌ Failed", "error": str(e)}
    return {"status": "❌ Unknown task"}
