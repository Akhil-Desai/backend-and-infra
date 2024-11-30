from pymongo import MongoClient
from dotenv import load_dotenv
import os

MongoDB = os.getenv("MONGO_URI")
client = MongoClient(MongoDB)
db = client.get_database("Todo")

def get_db():
    return db
