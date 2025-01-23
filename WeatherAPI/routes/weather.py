from models.weather import Weather
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from dependencies import get_redis_client, rate_limiter
import redis,json,requests,os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

@router.get("/{location}", dependencies=[Depends(rate_limiter)])
def weatherForLocation(location: str, cache: redis.Redis = Depends(get_redis_client)):


    cached_result = cache.get(location)
    if cached_result:
        print("Cache hit")
        return json.loads(cached_result)

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={api_key}"

    try:
        results = requests.get(url)
        data = results.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


    cache.set(location, json.dumps(data))
    return data
