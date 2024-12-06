from models.todos import Todo
from db import get_db
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()

#This should be a protected route needs to be edited to take a valid Token
@router.post("/")
def createTodo(todo: Todo, db=Depends(get_db)):
    todoCollection = db["todos"]
    try:
        todoDict = todo.model_dump()
        result = todoCollection.insert_one(todoDict)
        return {"message": "Succesfully created todo", "id": str(result.inserted_id)}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
