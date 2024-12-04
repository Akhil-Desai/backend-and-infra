import uuid
from pydantic import BaseModel, Field

class User(BaseModel):
    userName: str
    password: str
