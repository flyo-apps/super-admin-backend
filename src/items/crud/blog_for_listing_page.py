from fastapi import HTTPException
from typing import Optional
from datetime import datetime
import json

from items.models.blog_for_listing_page import BlogForListPageCreateBaseModel, BlogForListPageCreateModel, BlogForListPageUpdateBaseModel, BlogForListPageUpdateModel
from ..schemas.blog_for_listing_page import BlogsForListingPageSchema

from sqlalchemy.orm import Session
from db.aurora.aurora_base import CRUDBase


class BlogForListingPageCollection:
    def __init__(self):
        self.model = CRUDBase(BlogsForListingPageSchema)
    
    async def create_blog_for_listing_page(
        self,
        data: BlogForListPageCreateBaseModel,
        db: Session,
    ) -> any:
        try:
            where_clause = f"""code='{data.code}'"""
            existing_blog_for_listing_page = self.model.get_one(db=db, where_clause=where_clause)
            if existing_blog_for_listing_page is not None:
                return {"internal_response_code": 1, "message": f"""blog listing with code {data.code} exists"""}

            blog_for_listing_page_create = BlogForListPageCreateModel(**data.dict())
            blog_for_listing_page_create.screen_filter = json.loads(json.dumps(data.screen_filter).lower())
            created = self.model.create(db=db, obj_in=blog_for_listing_page_create)

            return {"internal_response_code": 0, "message": f"""created with code: {data.code}"""} if created else {"internal_response_code": 1, "message": f"""failed to create with code:{data.code}"""}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def update_blog_for_listing_page(
        self,
        data: BlogForListPageUpdateBaseModel,
        db: Session,
    ) -> any:
        try:
            where_clause = f"""code='{data.code}'"""
            existing_blog_for_listing_page = self.model.get_one(db=db, where_clause=where_clause)
            if existing_blog_for_listing_page is None:
                return {"internal_response_code": 1, "message": f"""data with code:{data.code} not found"""}

            if data.screen_filter is not None:
                data.screen_filter = json.loads(json.dumps(data.screen_filter).lower())

            blog_for_listing_page_update = BlogForListPageUpdateModel(**data.dict(exclude_unset=True))
            blog_for_listing_page_update.is_updated = True
            blog_for_listing_page_update.updated_at = datetime.now()
            updated = self.model.update(db=db, db_obj=existing_blog_for_listing_page, obj_in=blog_for_listing_page_update)
            
            return {"internal_response_code": 0, "message": f"""data with code:{data.code} updated"""} if updated else {"internal_response_code": 1, "message": f"""data with code:{data.code} failed to update"""}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
        
    async def get_blog_for_listing_page(
        self,
        db: Session,
        screen_filter: Optional[dict] = None,
        code: Optional[str] = None
    ) -> any:
        try:
            if screen_filter is not None:
                where_clause_dict = json.dumps(screen_filter, separators=(':', ': ')).lower()
                where_clause = f"""screen_filter::text='{where_clause_dict}'::text"""
            else:
                where_clause = f"""code='{code}'"""

            print(where_clause)
            exists = self.model.get_one(db=db, where_clause=where_clause)
            
            return {"internal_response_code": 0, "message": "success", "data": exists} if exists else {"internal_response_code": 1, "message": "failed", "data": None }
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def delete_blog_for_listing_page(
        self,
        code: str,
        db: Session,
    ) -> any:
        try:
            
            where_clause = f"""code='{code}'"""
            exists = self.model.get_one(db=db, where_clause=where_clause)
            if exists is None:
                return {"internal_response_code": 1, "message": f"""Code: {code}, not found"""}
            
            deleted = self.model.remove(db=db, where_clause=where_clause)
            
            return {"internal_response_code": 0, "message": f"""Code: {code}, deleted""", "data": None} if deleted == None else {"internal_response_code": 1, "message": f"""Failed to delete""", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")