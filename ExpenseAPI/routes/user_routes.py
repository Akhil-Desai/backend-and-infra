from fastapi import APIRouter,Depends,HTTPException
from db import get_db, assign_user_id
from models.user_models import User


router = APIRouter()


@router.post("/signup") #Create User
def sign_up(user: User, db = Depends(get_db)):
    #Hash password later, right now just testing auto increment
    user_collection = db["users"]
    new_user = {"username": user.username, "password": user.password, "user_id": assign_user_id(db)}
    #try inserting a new user
    try:
        user_collection.insert_one(new_user)

    except Exception as e:
        raise HTTPException(status_code="4xx", detail=str(e))

    return {"message": "new user created", "status code": "200"}
