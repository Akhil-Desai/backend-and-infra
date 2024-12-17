from pydantic import BaseModel


class Todo(BaseModel):
    task_id: int
    task: str
    due: str
    user_id: int
    is_done: bool = False
