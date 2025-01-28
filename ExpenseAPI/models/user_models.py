from pydantic import BaseModel


class User(BaseModel):
    username: str #Can be duplicate
    password: str #A Hashed/secure version will not be the raw string
