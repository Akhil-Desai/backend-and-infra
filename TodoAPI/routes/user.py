from models.user import User
from services.user import hashPassword,verifyPassword
from fastapi.security import OAuth2PasswordRequestForm
from db import get_db
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()

@router.post("/signup")
def createUser(user: User, db=Depends(get_db)):
    userCollection = db["users"]
    try:
        existing_user = userCollection.find_one({"userName": user.userName})
        if existing_user:
            return HTTPException(status_code=400, detail="Username already exist.")

        user.password = hashPassword(user.password)
        userDict = user.model_dump()
        result = userCollection.insert_one(userDict)
        return {"message": "Sucessfully created user", "id": str(result.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    userCollection = db["users"]
    try:
        findUser = userCollection.find_one({"userName": form_data.username})
        if not findUser or not verifyPassword(findUser["password"],form_data.password):
            return HTTPException(status_code=400, detail="Username or password is incorrect")

        return {"access_token": "TestToken123#" + findUser["userName"], "token_type": "bearer"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
