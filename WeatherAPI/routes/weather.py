from models.weather import Weather
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from dependencies import get_redis_client
import redis
import json


router = APIRouter()


@router.get("/{location}", response_model=Weather)
def weatherForLocation(location: str, cache: redis.Redis = Depends(get_redis_client)):

    TEST_LOCATIONS = {
        "London": {"date": "2025-02-01", "temperature": 40.6},
        "Barcelona": {"date": "2025-02-01", "temperature": 55.6},
    }


    result = cache.get(location)

    if result:
        print("Retrieved Cached result")
        return Weather(**json.loads(result))


    if location in TEST_LOCATIONS:
        cache.set(location, json.dumps(TEST_LOCATIONS[location]))
        return Weather(**(TEST_LOCATIONS[location]))

    return HTTPException(status_code=400, detail="Location not found")
