from pydantic import BaseModel

class User(BaseModel):
    userName: str
    password: str
