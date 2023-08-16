from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException

from items.models.quick_banners import QuickBannerCreateModel, QuickBannerUpdateModel

from sqlalchemy.orm import Session
from db.redis.redis_base import RedisBase
from ..schemas.quick_banners import QuickBannersSchema
from db.aurora.aurora_base import CRUDBase
import json
import uuid
from ..utils.constants import QUICK_BANNER_MAIN_KEY

class QuickBannersCollection:
    def __init__(self):
        self.model = CRUDBase(QuickBannersSchema)
        self.redis = RedisBase()
    
    async def create_quick_banners(
        self,
        screen_filter: dict,
        data: List[dict],
        db: Session,
    ) -> any:
        try:
            where_clause_dict = json.dumps(screen_filter, separators=(':', ': ')).lower()
            where_clause = f"""screen_filter::text='{where_clause_dict}'::text"""
            existing_quick_filter = self.model.get_one(db=db, where_clause=where_clause)
            if existing_quick_filter is not None:
                return {"internal_response_code": 1, "message": f"""Quick Filter {screen_filter} already exists"""}

            quick_filter_create = QuickBannerCreateModel(code=str(uuid.uuid4()), screen_filter=json.loads(json.dumps(screen_filter).lower()), data=data)
            created_quick_filter = self.model.create(db=db, obj_in=quick_filter_create)

            if created_quick_filter:
                await self.redis.hset_list_dict(main_key=QUICK_BANNER_MAIN_KEY,sub_key=json.loads(json.dumps(screen_filter).lower()), list_data=data)

            return {"internal_response_code": 0, "message": f"""Quick Filter  {screen_filter} created"""} if created_quick_filter else {"internal_response_code": 1, "message": f"""Failed to create quick filter {screen_filter}"""}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def update_quick_banners(
        self,
        screen_filter: dict,
        data: List[dict],
        db: Session,
    ) -> any:
        try:
            where_clause_dict = json.dumps(screen_filter, separators=(':', ': ')).lower()
            where_clause = f"""screen_filter::text='{where_clause_dict}'::text"""
            existing_quick_filter = self.model.get_one(db=db, where_clause=where_clause)
            if existing_quick_filter is None:
                return {"internal_response_code": 1, "message": f"""Quick Filter {screen_filter} not found"""}

            quick_filter_update = QuickBannerUpdateModel(data=data)
            quick_filter_update.is_updated = True
            quick_filter_update.updated_at = datetime.now()
            updated_quick_filter = self.model.update(db=db, db_obj=existing_quick_filter,obj_in=quick_filter_update)

            if updated_quick_filter:
                await self.redis.hset_list_dict(main_key=QUICK_BANNER_MAIN_KEY,sub_key=json.loads(json.dumps(screen_filter).lower()), list_data=data)
            
            return {"internal_response_code": 0, "message": f"""Quick Filter  {screen_filter} updated"""} if updated_quick_filter else {"internal_response_code": 1, "message": f"""Failed to udpate quick filter {screen_filter}"""}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
        
    async def get_quick_banners(
        self,
        screen_filter: dict,
        db: Session,
    ) -> any:
        try:
            quick_filter = await self.redis.hget_list_dict(main_key=QUICK_BANNER_MAIN_KEY, sub_key=json.loads(json.dumps(screen_filter).lower()))
            if quick_filter is not None:
                return {"internal_response_code": 0, "message": "success", "data": {"data": quick_filter,"screen_filter": screen_filter } }

            where_clause_dict = json.dumps(screen_filter, separators=(':', ': ')).lower()
            where_clause = f"""screen_filter::text='{where_clause_dict}'::text"""
            existing_quick_filter = self.model.get_one(db=db, where_clause=where_clause)
            if existing_quick_filter is None:
                return {"internal_response_code": 1, "message": f"""Quick Filter {screen_filter} not found""", "data": None}

            await self.redis.hset_list_dict(main_key=QUICK_BANNER_MAIN_KEY,sub_key=json.loads(json.dumps(screen_filter).lower()), list_data=existing_quick_filter.__dict__["data"])

            return {"internal_response_code": 0, "message": "success", "data":existing_quick_filter }
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def delete_quick_banners(
        self,
        screen_filter: dict,
        db: Session,
    ) -> any:
        try:
            where_clause_dict = json.dumps(screen_filter, separators=(':', ': ')).lower()
            where_clause = f"""screen_filter::text='{where_clause_dict}'::text"""
            existing_quick_filter = self.model.get_one(db=db, where_clause=where_clause)
            if existing_quick_filter is None:
                return {"internal_response_code": 1, "message": f"""Quick Filter {screen_filter} not found"""}
            
            updated_quick_filter = self.model.remove(db=db, where_clause=where_clause)

            if updated_quick_filter == None:
                await self.redis.hdel_list_dict(main_key=QUICK_BANNER_MAIN_KEY,sub_key=json.loads(json.dumps(screen_filter).lower()))
            
            return {"internal_response_code": 0, "message": f"""Quick Filter  {screen_filter} deleted"""} if updated_quick_filter == None else {"internal_response_code": 1, "message": f"""Failed to delete quick filter {screen_filter}"""}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")