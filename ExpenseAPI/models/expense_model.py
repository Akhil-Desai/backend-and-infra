from pydantic import BaseModel, Field
from enum import Enum

class ExpenseType(str, Enum):
    Groceries = "groceries"
    Leisure = "leisure"
    Electronics = "electronics"
    Utilities = "utilities"
    Clothing = "clothing"
    Health = "health"
    Others = "others"



class Expense(BaseModel):
    type: ExpenseType
    amount: float = Field(..., gt=0)
    date: str = None
    user_id: int = None #Foreign Key
    expense_id: int
