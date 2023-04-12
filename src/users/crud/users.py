from typing import Optional, Type
from db.mongo.collections import USERS
from ..models.users import UD, UserOutModel
from db.mongo.mongo_base import MongoBase
from db.redis.redis_base import RedisBase
from users.utils.constants import USERS_REDIS
import base64
import os
from fastapi import HTTPException
from hashlib import blake2b

class MongoDBUserDatabase:
    def __init__(self, user_db_model: Type[UD]):
        self.user_db_model = user_db_model
        self.redis = RedisBase()
        self.collection = MongoBase()
        self.collection(USERS)

    async def find_by_username(self, username: str) -> Optional[UD]:
        try:
            user = await self.redis.hget("users", username)
            if user != None:
                return UserOutModel(**user)

            user_model= await self.collection.find_one(
                {"username": username},
                return_doc_id=True,
                extended_class_model=UserOutModel,
            )

            if user_model != None and user_model.is_deleted != True:
                await self.redis.hset(USERS_REDIS, username, user_model.dict())

            return user_model
        except Exception as e:
            raise e

    async def get_username_hash(
        self,
        username: str
    ) -> any:
        try:
            secret_key = base64.b64encode(
                bytes(os.environ.get("USERNAME_PRIVATE_KEY"), 'utf-8'))
            h = blake2b(key=secret_key, digest_size=5)
            username_bytes = base64.b64encode(bytes(username, 'utf-8'))
            h.update(username_bytes)
            return h.hexdigest()
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
