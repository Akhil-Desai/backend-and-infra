import uuid
from pydantic import BaseModel, Field

class User(BaseModel):
    userName: str
    password: str
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
