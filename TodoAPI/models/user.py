import uuid
from pydantic import BaseModel, Field

class User(BaseModel):
    userName: str | None = None
    password: str | None = None
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
