from fastapi import APIRouter, Depends, Request, HTTPException
from models.expense_model import Expense
from utils import get_current_user
from db import get_db
from datetime import datetime


router = APIRouter()


@router.post("/new_expense")
def create_expense(expense: Expense, current_user = Depends(get_current_user), db = Depends(get_db)):
    expenses_collection = db['expenses']

    try:
        new_expense = {"type": expense.type, "amount": expense.amount, "date": str(datetime.utcnow), "user_id": current_user }
        expenses_collection.insert_one(new_expense)

    except HTTPException as e:
        raise HTTPException(status_code="400", detail=str(e))
