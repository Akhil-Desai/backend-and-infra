from pydantic import BaseModel


class Todo(BaseModel):
    task_id: int
    task: str
    due: str
    userName: str
    is_done: bool = False
