from pydantic import BaseModel

class Expense(BaseModel):
    type: str
    amount: float
    date: str
    user_id: int #Foreign Key
