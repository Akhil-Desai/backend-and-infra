from fastapi import APIRouter,Depends,HTTPException
from db import get_db, assign_user_id
from models.user_models import User
from utils import hash_password, verify_password


router = APIRouter()


@router.post("/signup") #Create User
def sign_up(user: User, db = Depends(get_db)):

    hashed_password = hash_password(user.password)

    user_collection = db["users"]
    new_user = {"username": user.username, "password": hashed_password, "user_id": assign_user_id(db)}
    #try inserting a new user
    try:
        user_collection.insert_one(new_user)

    except Exception as e:
        raise HTTPException(status_code="4xx", detail=str(e))

    return {"message": "new user created", "status code": "200"}

@router.post("/login")
def login(user: User, db= Depends(get_db)):

    user_collection = db["users"]

    retrieved_user =  user_collection.find_one({"username": user.username})

    if verify_password(user.password, retrieved_user["password"]):
        #Return JWT Token to user
        pass

    else:
        raise HTTPException(200, detail="Wrong password!")

    return {"message": "success"}
