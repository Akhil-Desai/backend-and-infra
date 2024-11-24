from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

MongoDB = os.getenv("MONGO_URI")
client = MongoClient(MongoDB)
db = client.get_database("Todo")


@app.get("/db-health")
def db_health_check():
    """Ping the database to check the connection."""
    try:
        # MongoDB ping command
        result = db.command("ping")
        return {"status": "connected", "ping": result}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Define a route
@app.get("/")
def read_root():
    return {"message": "Hello, MongoDB with FastAPI!"}
