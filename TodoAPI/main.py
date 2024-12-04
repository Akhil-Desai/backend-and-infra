from fastapi import FastAPI
from db import get_db
from typing import Annotated

from routes.user import router as user_router

app = FastAPI()

app.include_router(user_router,prefix="/users/v1", tags=["users"])



@app.get("/db-health")
def db_health_check():
    """Ping the database to check the connection."""
    try:
        db = get_db()
        result = db.command("ping")
        return {"status": "connected", "ping": result}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/")
def read_root():
    return {"message": "Hello, MongoDB with FastAPI!"}
