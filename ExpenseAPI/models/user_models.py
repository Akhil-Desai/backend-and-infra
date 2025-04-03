from pydantic import BaseModel


class User(BaseModel):
    username: str #enforcing unique since we don't have a field to uniquely identify
    password: str #A Hashed/secure version, will not be the raw string
    user_id: int = None #
