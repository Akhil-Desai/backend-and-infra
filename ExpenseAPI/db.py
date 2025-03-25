from pymongo import MongoClient
from fastapi import Depends, HTTPException
import os

Mongo = os.getenv("MONGO_URI")
client = MongoClient(Mongo)

def get_db():
    db = client.get_database("Expenses")
    return db

def assign_id(db = Depends(get_db)):
    counter_collection = db["counter"]

    current_seq = counter_collection.find_one({"flag": 1})

    if current_seq is None:
        current_seq = {"flag": 1, "seq": 0}
        counter_collection.insert_one(current_seq)

    counter_collection.update_one({"flag": 1}, {'$inc': {"seq": 1}})

    return current_seq["seq"]


db = get_db()
db.expenses.create_index([("user_id", 1)])
# db.expenses.create_index(["expense_id", 1])
db.expenses.create_index([("username", "text")])
