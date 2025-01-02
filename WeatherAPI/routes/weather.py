from models.weather import Weather
from fastapi import APIRouter, Depends, HTTPException, Request, Query


router = APIRouter()


@router.get("/{location}", response_model=Weather)
def weatherForLocation(location: str):

    TEST_LOCATIONS = {
        "London": {"date": "2025-02-01",
        "temperature": 40.6},
        "Barcelona": {"date": "2025-02-01",
        "temperature": 55.6},
    }

    return {
        "date": TEST_LOCATIONS[location]["date"],
        "temperature": TEST_LOCATIONS[location]["temperature"]
    }
