import redis


def get_redis_client():
    client = redis.Redis(host="localhost", port=6379, db=0 )
    try:
        yield client
    finally:
        client.close()
