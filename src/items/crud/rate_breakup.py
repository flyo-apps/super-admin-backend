from typing import List, Optional
from datetime import datetime
from sqlalchemy import exc
from fastapi import HTTPException

from items.models.rate_breakup import RateBreakupCreateModel, RateBreakupUpdateModel, RateBreakupDeleteModel

from sqlalchemy.orm import Session
from db.redis.redis_base import RedisBase
from ..schemas.rate_breakup import RateBreakupSchema
from db.aurora.aurora_base import CRUDBase
import json
import uuid
from ..utils.constants import QUICK_FILTER_MAIN_KEY

class RateBreakupCollection:
    def __init__(self):
        self.model = CRUDBase(RateBreakupSchema)
    
    async def create_rate_breakup(
        self,
        create_rate_breakup: dict,
        db: Session,
    ) -> any:
        try:
            where_clause = f"""code='{create_rate_breakup["code"]}'"""
            existing_rate_breakup = self.model.get_one(db=db, where_clause=where_clause)
            if existing_rate_breakup is not None:
                return {"internal_response_code": 1, "message": f"""Rate with code {create_rate_breakup["code"]} exists""", "data": None}

            rate_breakup_create = RateBreakupCreateModel(**create_rate_breakup)
            created_rate_breakup = self.model.create(db=db, obj_in=rate_breakup_create)

            return {"internal_response_code": 0, "message": f"""created story {create_rate_breakup["code"]}"""} if created_rate_breakup else {"internal_response_code": 1, "message": f"""failed to create story {create_rate_breakup["code"]}"""}
        except Exception as e:
            if type(e) == exc.IntegrityError:
                return {"internal_response_code": 1, "message": "A rate already exist with same brand and metal", "data": None}
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def update_rate_breakup(
        self,
        update_rate_breakup: dict,
        db: Session,
    ) -> any:
        try:
            where_clause = f"""code='{update_rate_breakup["code"]}' AND is_deleted=false"""
            existing_rate_breakup = self.model.get_one(db=db, where_clause=where_clause)
            if existing_rate_breakup is None:
                return {"internal_response_code": 1, "message": f"""Rate Break with code: {update_rate_breakup["code"]}, Not Found"""}

            rate_breakup_update = RateBreakupUpdateModel(**update_rate_breakup)
            rate_breakup_update.is_updated = True
            rate_breakup_update.updated_at = datetime.now()
            updated_rate_breakup = self.model.update(db=db, db_obj=existing_rate_breakup, obj_in=rate_breakup_update)
            
            return {"internal_response_code": 0, "message": f"""story {update_rate_breakup["code"]} updated"""} if updated_rate_breakup else {"internal_response_code": 1, "message": f"""failed to update story {update_rate_breakup["code"]}"""}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def get_rate_breakup_by_code(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""(code='{code}' AND is_deleted=false)"""
            existing_rate_breakup = self.model.get_one(db=db, where_clause=where_clause)

            return {"internal_response_code": 0, "message": f"""Success""", "data": existing_rate_breakup} if existing_rate_breakup else {"internal_response_code": 0, "message": f"""Failed""", "data": None}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def delete_rate_breakup_by_code(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{code}' AND is_deleted=false"""
            existing_rate_breakup = self.model.get_one(db=db, where_clause=where_clause)
            if existing_rate_breakup is None:
                return {"internal_response_code": 1, "message": f"""Rate Breakup with code: {code}, Not found"""}

            rate_breakup_delete_dict = RateBreakupDeleteModel(code=code).dict()
            deleted_rate_breakup = self.model.update(db=db, db_obj=existing_rate_breakup, obj_in=rate_breakup_delete_dict)

            return {"internal_response_code": 0, "message": f"""Rate Breakup {code} deleted""", "data": "None"} if deleted_rate_breakup else {"internal_response_code": 1, "message": f"""Failed to delete Rate Breakup {code}""", "data": None}
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def get_all_rate_breakup(
        self,
        db: Session
    ) -> any:
        try:
            where_clause = f"""is_deleted=false"""
            all_rate_breakup = self.model.get_all(db=db, where_clause=where_clause, skip=0, limit=200)
            if all_rate_breakup is None:
                return {"internal_response_code": 1, "message": f"""Failed""", "data": None}
            
            return {"internal_response_code": 0, "message": f"""Success""", "data":  all_rate_breakup} if all_rate_breakup else {"internal_response_code": 1, "message": f"""Failed""", "data": None}
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def get_all_rate_breakup_by_brand_and_or_metal(
        self,
        db: Session,
        brand: Optional[str] = None,
        metal: Optional[str] = None,
    ) -> any:
        try:
            where_clause = f"""is_deleted=false"""
            if brand != None:
                where_clause = where_clause + f""" AND brand='{brand}'"""
            
            if metal != None:
                where_clause = where_clause + f""" AND metal='{metal}'"""

            all_rate_breakup = self.model.get_all(db=db, where_clause=where_clause, skip=0, limit=200)
            if all_rate_breakup is None:
                return {"internal_response_code": 1, "message": f"""Failed""", "data": None}
            
            return {"internal_response_code": 0, "message": f"""Success""", "data":  all_rate_breakup} if all_rate_breakup else {"internal_response_code": 1, "message": f"""Failed""", "data": None}
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")
    

    