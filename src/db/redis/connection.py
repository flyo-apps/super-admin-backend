import redis
import os

# r = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), db=0)

redis_connection = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"))

def get_redis_client():
    try:
        return redis_connection
    except Exception as e:
        return e