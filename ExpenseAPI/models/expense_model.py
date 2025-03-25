from pydantic import BaseModel

class Expense(BaseModel):
    type: str
    amount: float
    date: str = None
    user_id: int = None #Foreign Key
    expense_id: int
