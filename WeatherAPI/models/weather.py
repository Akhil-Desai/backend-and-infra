from pydantic import BaseModel

class Weather(BaseModel):
    date: str
    temperature: float
