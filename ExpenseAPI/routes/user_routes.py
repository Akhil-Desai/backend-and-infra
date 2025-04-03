from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from db import get_db, assign_id
from models.user_models import User
from utils import hash_password, verify_password
from datetime import datetime, timedelta
import jwt


router = APIRouter()


@router.post("/signup") #Create User
def sign_up(user: User, db = Depends(get_db)):

    hashed_password = hash_password(user.password)

    user_collection = db["users"]

    if user_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=200, detail="Username already exist, please choose a different one")

    new_user = {"username": user.username, "password": hashed_password, "user_id": assign_id(db)}
    #try inserting a new user
    try:
        user_collection.insert_one(new_user)

    except Exception as e:
        raise HTTPException(status_code="4xx", detail=str(e))

    return {"message": "new user created", "status code": "200"}

@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), db= Depends(get_db)):

    user_collection = db["users"]

    retrieved_user =  user_collection.find_one({"username": user.username})


    if retrieved_user and verify_password(user.password, retrieved_user["password"]):
        encoded_jwt = jwt.encode({"sub": str(retrieved_user["user_id"]), "exp": datetime.utcnow() + timedelta(minutes=30)}, "secret", algorithm="HS256")
        return {"access_token": encoded_jwt, "token_type": "bearer"}

    else:
        raise HTTPException(400, detail="Wrong password!")
