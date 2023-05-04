from typing import List
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

    async def hdel(
        self,
        main_key: str,
        sub_key: str
    ):
        try:
            deleted = self.redis.hdel(main_key, sub_key)
            return True if deleted else None
        except Exception:
            return None

    async def delete_list(
        self,
        main_key: str
    ):
        try:
            deleted = self.redis.delete(main_key)
            return True if deleted else None
        except Exception:
            return None

    async def lpush(
        self,
        main_key: str,
        data: dict
    ):
        try:
            encoded_data = json.dumps(data, default=str).encode('utf-8')

            hset_done = self.redis.lpush(main_key, encoded_data)

            if hset_done == 0:
                return "updated"
            elif hset_done == 1:
                return "created"
            else:
                return "failed"
        except Exception:
            return None

    async def rpush(
        self,
        main_key: str,
        data: dict
    ):
        try:
            encoded_data = json.dumps(data, default=str).encode('utf-8')
            hset_done = self.redis.rpush(main_key, encoded_data)

            if hset_done == 0:
                return "updated"
            elif hset_done == 1:
                return "created"
            else:
                return "failed"
        except Exception:
            return None

    async def lrange(
        self,
        main_key: str,
        start: int,
        end: int
    ):
        try:
            encoded_data = self.redis.lrange(main_key,start, end)
            return encoded_data if encoded_data else []
        except Exception:
            return None

    async def sadd(
        self,
        main_key: str,
        value: str
    ):
        try:
            inserted = self.redis.sadd(main_key, value)
            if inserted == 0:
                return "updated"
            elif inserted == 1:
                return "created"
            else:
                return "failed"
        except Exception:
            return None

    async def smembers(
        self,
        main_key: str
    ):
        try:
            encoded_data = self.redis.smembers(main_key)
            data = list(encoded_data)
            for index,items in enumerate(data):
                data[index] = items.decode('utf-8')
            return data  if data else []
        except Exception:
            return None

    async def lrem(
        self,
        main_key: str,
        count: int,
        value: str
    ):
        try:
            encoded_data = json.dumps(value, default=str).encode('utf-8')
            returned_val = self.redis.lrem(main_key, count, encoded_data)

            if returned_val == 1:
                return "removed"
            else:
                return "failed"
            
        except Exception:
            return None
    
    async def ltrim(
        self,
        main_key: str,
        start: int,
        end: int
    ):
        try:
            returned_val = self.redis.ltrim(main_key, start, end)
            if returned_val == 1:
                return "removed"
            else:
                return "failed"
        except Exception:
            return None

    async def hset_list_dict(
        self,
        main_key: str,
        sub_key: str,
        list_data: List[dict]
    ):
        try:
            encoded_data = json.dumps(list_data, default=str).encode('utf-8')
            sub_key_string = json.dumps(sub_key, default=str).encode('utf-8')

            hset_done = self.redis.hset(main_key, sub_key_string,  encoded_data)

            if hset_done == 0:
                return "updated"
            elif hset_done == 1:
                return "created"
            else:
                return "failed"

        except Exception as e:
            print(e, "hello")
            return None

    async def hget_list_dict(
        self,
        main_key: str,
        sub_key: str
    ):
        try:
            sub_key_string = json.dumps(sub_key, default=str).encode('utf-8')
            encoded_data = self.redis.hget(main_key, sub_key_string)
            data = json.loads(encoded_data)
            return data if encoded_data else None
        except Exception:
            return None

    async def hdel_list_dict(
        self,
        main_key: str,
        sub_key: str
    ):
        try:
            sub_key_string = json.dumps(sub_key, default=str).encode('utf-8')
            deleted = self.redis.hdel(main_key, sub_key_string)
            return True if deleted else None
        except Exception:
            return None