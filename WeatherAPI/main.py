from fastapi import FastAPI

from routes.weather import router as router_weather


app = FastAPI()

app.include_router(router_weather, prefix="/weather/v1", tags=["weather"])
