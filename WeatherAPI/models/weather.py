from pydantic import BaseModel
from types import List

class Weather(BaseModel):
    date: str
    temperature: float
