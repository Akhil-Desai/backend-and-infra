import redis
from fastapi import Depends,Request,HTTPException
import time
import json


def get_redis_client():
    client = redis.Redis(host="localhost", port=6379, db=0 )
    try:
        yield client
    finally:
        client.close()

def rate_limiter(request: Request, cache: redis.Redis = Depends(get_redis_client), limit: int=5, buffer: int=60):

    client_ip = request.client.host

    client_request = cache.get(client_ip)
    if not client_request:
        cache.set(client_ip, json.dumps({"calls": 1}), ex=buffer)
        return

    client_request = json.loads(client_request)
    client_request['calls'] = int(client_request['calls'])

    if (client_request['calls']) < limit:
        print(client_request)
        client_request['calls'] += 1
        cache.set(client_ip, json.dumps(client_request), ex=buffer)

    else:
        raise HTTPException(status_code=400, detail="Rate limit exceeded. Please wait before making more request")
