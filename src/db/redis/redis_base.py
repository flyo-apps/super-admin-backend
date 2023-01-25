import json
from db.redis.connection import get_redis_client

class RedisBase:
    def __init__(self):
        self.redis =  get_redis_client()

    async def hset(
        self, 
        main_key: str, 
        sub_key: str, 
        data: dict
    ):
        try:
            encoded_data = json.dumps(data, default=str).encode('utf-8')

            hset_done = self.redis.hset(main_key, sub_key,  encoded_data)

            if hset_done == 0:
                return "updated"
            elif hset_done == 1:
                return "created"
            else:
                return "failed"

        except Exception:
            return None
    
    async def hget(
        self,
        main_key: str,
        sub_key: str
    ):
        try:
            encoded_data = self.redis.hget(main_key, sub_key)
            data = json.loads(encoded_data)
            return data if encoded_data else None
        except Exception:
            return None