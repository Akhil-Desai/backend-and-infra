from models.todos import Todo
from db import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from services.todo import verifyToken


router = APIRouter()

#These should all be a protected route needs to be edited to take a valid Token
@router.post("/")
async def createTodo(request: Request, todo: Todo, db=Depends(get_db)):
    todoCollection = db["todos"]
    body = await request.json()
    try:
        auth_token = body.get("Authorization")
        if not auth_token or not verifyToken(auth_token):
            return HTTPException(status_code=400, detail="Unauthorized User")
        todoDict = todo.model_dump()
        result = todoCollection.insert_one(todoDict)
        return {"message": "Successfully created todo item", "id": str(result.inserted_id)}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@router.put("/{todo_id}")
async def updateTodo(request: Request, todo: Todo, todo_id: int, db=Depends(get_db)):
    todoCollection = db["todos"]
    body = await request.json()

    try:
        auth_token = body.get("Authorization")
        if not auth_token or not verifyToken(auth_token):
            return HTTPException(status_code=400, detail="Unauthorized User")
        updateItem = todoCollection.update_one({"todo_id": todo_id}, {"$set": todo.model_dump()})
        if not updateItem.modified_count == 0:
            return HTTPException(status_code=(400), detail="Todo Item doesn't exist")

        return {"message": "Successfully updated todo item"}

    except Exception as e :
        return HTTPException(status_code=500, detail=str(e))

@router.delete("/{todo_id}")
async def deleteTodo(request: Request, todo_id: int, db=Depends(get_db)):
    todoCollection = db["todos"]
    body = await request.json()

    try:
        auth_token = body.get("Authorization")
        if not auth_token or not verifyToken(auth_token):
            return HTTPException(status_code=400, detail="Unauthorized User")
        deleteItem = todoCollection.delete_one({"todo_id": todo_id})
        if deleteItem.delete_count == 0:
            return HTTPException(status_code=(400), detail="Todo Item doesn't exist")

        return {"message": "Successfully deleted todo item"}

    except Exception as e :
        return HTTPException(status_code=500, detail=str(e))


@router.get("/myTodos")
async def getTodos(request: Request, db = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(0, ge=1, le=100)):
    todoCollection = db["todos"]
    body = await request.json()

    try:
        auth_token = body.get("Authorization")
        if not auth_token or not verifyToken(auth_token):
            return HTTPException(status_code=400, detail="Unauthorized User")
        userName = auth_token.split('#')[0]
        usersTodos = list(todoCollection.find({"userName": userName}).skip(skip).limit(limit))
        if not usersTodos:
            return HTTPException(status_code=(400), detail="Todo items doesn't exist")
        return {"Your Todos": usersTodos}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
