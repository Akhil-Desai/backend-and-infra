from fastapi import FastAPI, Depends,HTTPException
from db import get_db
from routes.user_routes import router as user_router
from routes.expenses_routes import router as expense_router

app = FastAPI()

app.include_router(user_router, prefix="/user/v1")
app.include_router(expense_router, prefix="/expenses/v1")


@app.get("/db-health")
def health_check(db = Depends(get_db)):
    result = db.command("ping")
    return {"message": "status connected", "ping": result}
