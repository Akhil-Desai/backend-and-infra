from models.user import User
from db import get_db
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()

@router.post("/")
def createUser(user: User, db=Depends(get_db)):
    userCollection = db["users"]
    try:
        userDict = user.model_dump()
        result = userCollection.insert_one(userDict)
        return {"message": "Sucessfully created user", "id": str(result.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
