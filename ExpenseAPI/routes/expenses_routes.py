from fastapi import APIRouter, Depends, Request, HTTPException
from models.expense_model import Expense
from utils import get_current_user
from db import get_db, assign_id
from datetime import datetime


router = APIRouter()


@router.post("/")
def create_expense(expense: Expense, current_user = Depends(get_current_user), db = Depends(get_db)):
    expenses_collection = db['expenses']

    try:
        new_expense = {"type": expense.type, "amount": expense.amount, "date": str(datetime.utcnow), "user_id": int(current_user), "expense_id": assign_id(db) }
        expenses_collection.insert_one(new_expense)

    except HTTPException as e:
        raise HTTPException(status_code="400", detail=str(e))

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db=Depends(get_db), current_user= Depends(get_current_user)):
    expenses_collection = db['expenses']

    try:
        delete_expense = expenses_collection.find_one({"expense_id": expense_id})
        if not delete_expense:
            raise HTTPException(status_code="404", detail="Expense not found")

        if int(current_user) != delete_expense["user_id"]:
            raise HTTPException(status_code="404", detail="User is not authorized to delete this expense")

        expenses_collection.delete_one({"expense_id": expense_id})
        return {"message": "Expense deleted successfully"}

    except HTTPException as e:
        raise HTTPException(status_code="400", detail=(e))

@router.put("/{expense_id}")
def update_expense(expense_id: int, updated_expense: Expense, db=Depends(get_db), current_user=Depends(get_current_user),):
    expenses_collection = db['expenses']

    try:
        resource = expenses_collection.find_one({"expense_id": expense_id})

        if not resource:
            raise HTTPException(status_code="404", detail="Expense not found")

        if int(current_user) != resource["user_id"]:
            raise HTTPException(status_code="404", detail="User not authorized to update resource")

        update_data = updated_expense.dict(exclude_none=True,exclude={"user_id", "expense_id"})

        result = expenses_collection.update_one({"expense_id": expense_id}, {"$set": update_data})
        return {"message": "Successfully updated expense"}

    except HTTPException as e:
        raise HTTPException(status_code="404", detail=(e))


