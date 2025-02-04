from fastapi import APIRouter, Depends, Request
from models.expense_model import Expense
from db import get_db


router = APIRouter()


@router.post("/expenses", )
def create_expense(expense: Expense, db = Depends(get_db)):
    expenses_collection = db['expenses']


    #Validate JWT Token and extract user_id
