from models.todos import Todo
from db import get_db
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()

#These should all be a protected route needs to be edited to take a valid Token
@router.post("/")
def createTodo(todo: Todo, db=Depends(get_db)):
    todoCollection = db["todos"]
    try:
        todoDict = todo.model_dump()
        result = todoCollection.insert_one(todoDict)
        return {"message": "Successfully created todo item", "id": str(result.inserted_id)}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.put("/{todo_id}")
def updateTodo(todo: Todo, todo_id: int, db=Depends(get_db)):
    todoCollection = db["todos"]
    try:
        updateItem = todoCollection.update_one({"todo_id": todo_id}, {"$set": todo.model_dump()})
        if not updateItem.modified_count == 0:
            return HTTPException(status_code=(400), detail="Todo Item doesn't exist")

        return {"message": "Successfully updated todo item"}

    except Exception as e :
        return HTTPException(status_code=500, detail=str(e))

@router.delete("/{todo_id}")
def deleteTodo(todo_id: int, db=Depends(get_db)):
    todoCollection = db["todos"]
    try:
        deleteItem = todoCollection.delete_one({"todo_id": todo_id})
        if deleteItem.delete_count == 0:
            return HTTPException(status_code=(400), detail="Todo Item doesn't exist")

        return {"message": "Successfully deleted todo item"}

    except Exception as e :
        return HTTPException(status_code=500, detail=str(e))
