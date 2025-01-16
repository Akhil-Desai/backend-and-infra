from models.weather import Weather
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from dependencies import get_redis_client
import redis,json,requests,os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

@router.get("/{location}", response_model=Weather)
def weatherForLocation(location: str, cache: redis.Redis = Depends(get_redis_client)):

    #TODO: Try hitting the cache first before making the API call

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={api_key}"

    try:
        results = requests.get(url)

    except:
        return "Error" #TODO: Return error code, need to know structure/output of results
    finally:
        return results #TODO: Return neccesary data, and set data to cache

