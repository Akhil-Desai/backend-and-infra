from pydantic import BaseModel


class Todo(BaseModel):
    task: str
    due: str
    user_id: int | str
    is_done: bool = False
