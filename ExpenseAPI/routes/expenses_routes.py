from fastapi import APIRouter, Depends, Request, HTTPException
from models.expense_model import Expense
from utils import get_current_user
from db import get_db, assign_id
from datetime import datetime


router = APIRouter()


@router.post("/new/expense")
def create_expense(expense: Expense, current_user = Depends(get_current_user), db = Depends(get_db)):
    expenses_collection = db['expenses']

    try:
        new_expense = {"type": expense.type, "amount": expense.amount, "date": str(datetime.utcnow), "user_id": int(current_user), "expense_id": assign_id(db) }
        expenses_collection.insert_one(new_expense)

    except HTTPException as e:
        raise HTTPException(status_code="400", detail=str(e))

@router.post("/delete/expense")
def delete_expense(expense_id: int, db=Depends(get_db), current_user= Depends(get_current_user)):
    expenses_collection = db['expenses']

    try:
        delete_expense = expenses_collection.find_one({"expense_id": expense_id})
        if not delete_expense:
            raise HTTPException(status_code="404", detail="Expense not found")

        if current_user != delete_expense["user_id"]:
            raise HTTPException(status_code="404", detail="User is not authorized to delete this expense")

        expenses_collection.delete_one({"expense_id": expense_id})
        return {"message": "Expense deleted successfully"}

    except HTTPException as e:
        raise HTTPException(status_code="400", detail=(e))
