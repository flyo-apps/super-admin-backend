from datetime import datetime
from fastapi import HTTPException
from ..utils.constants import HOMEPAGE_COLLECTION_COL_RETURN
from .categories import CategoriesCollection
from ..models.homepage_group import (
    CreateHomePageCollectionBaseModel,
    CreateHomePageCollectionModel,
    UpdateHomePageCollectionBaseModel,
    UpdateHomePageCollectionModel
)

from ..schemas.homepage_group import HomePageCollectionsSchema
from sqlalchemy.orm import Session
from db.aurora.aurora_base import CRUDBase

class HomepageGroupCollection:
    def __init__(self):
        self.model = CRUDBase(HomePageCollectionsSchema)

    # async def get_redirect_to_by_redirect_name(
    #     self,
    #     db: Session,
    #     redirect_name: str
    # ) -> any:
    #     try:
    #         categories_collection = CategoriesCollection()

    #         redirect_details = await categories_collection.get_category_by_name(db=db, name=redirect_name)

    #         return redirect_details.code if redirect_details else None
    #     except Exception:
    #         raise HTTPException(status_code=500, detail="Something went wrong")


    # async def create_homepage_collection(
    #     self,
    #     db: Session,
    #     homepage_collection_details: CreateHomePageCollectionBaseModel
    # ) -> any:
    #     try:
    #         if_exists = await self.get_homepage_collection_by_code_and_name(db=db, name=homepage_collection_details.homepage_collection_name, code=homepage_collection_details.code)
    #         if if_exists:
    #             return {"internalResponseCode": 1, "message": "A Collection already exists with the Title"}
                
    #         redirect_to_code = await self.get_redirect_to_by_redirect_name(db=db, redirect_name=homepage_collection_details.redirect_name)

    #         if redirect_to_code is None:
    #             return

    #         homepage_collection_create = CreateHomePageCollectionModel(**homepage_collection_details.dict(exclude_unset=True))
    #         homepage_collection_create.redirect_to = redirect_to_code

    #         created_homepage_collection = self.model.create(db=db, obj_in=homepage_collection_create)

    #         return {"internal_response_code": 0, "message": "Homepage Collection Created"} if created_homepage_collection else {"internal_response_code": 1, "message": "Homepage Collection Not Created, some error occurred"}

    #     except Exception:
    #         raise HTTPException(status_code=500, detail="Something went wrong")


    # async def update_homepage_collection(
    #     self,
    #     update_details: UpdateHomePageCollectionBaseModel,
    #     db: Session
    # ) -> any:
    #     try:
            
    #         home_page_collection = await self.get_homepage_collection_by_code(db=db, collection_code=update_details.code)
           
    #         if home_page_collection is None:
    #             return {"internal_response_code": 1, "message": "No home page collection found"}

    #         update_details_final = UpdateHomePageCollectionModel(**update_details.dict(exclude_unset=True))
            
    #         if update_details_final.homepage_collection_name is not None:
    #             update_details_final.homepage_collection_name = update_details_final.homepage_collection_name.strip()
                
    #         if update_details_final.collection_info is not None:
    #             update_details_final.collection_info = update_details_final.collection_info.strip()

    #         if update_details_final.redirect_type is not None:
    #             update_details_final.redirect_type = update_details_final.redirect_type.strip()

    #         if update_details_final.redirect_name is not None:
    #             redirect_to_id = await self.get_redirect_to_by_redirect_name(db=db, redirect_name=update_details.redirect_name)

    #             if redirect_to_id is not None:
    #                 update_details_final.redirect_name = update_details.redirect_name.strip()
    #                 update_details_final.redirect_to = redirect_to_id

    #         update_details_final.is_updated = True
    #         update_details_final.updated_at = datetime.now()
    #         updated_home_page_collection = self.model.update(db=db, db_obj=home_page_collection, obj_in=update_details_final)

    #         return {"internal_response_code": 0, "message": "Home Page collection updated"} if updated_home_page_collection else {"internal_response_code": 1, "message": "Home Page Collection Not Updated"}
    #     except Exception:
    #         raise HTTPException(status_code=500, detail="Something went wrong")

    # async def get_all_homepage_collections(
    #     self,
    #     page: int,
    #     limit: int,
    #     db: Session
    # ) -> any:
    #     try:
    #         where_clause = f"""(is_deleted = False)"""
    #         sorting_method = "updated_at"
    #         if page == 1:
    #             skip = 0
    #         else:
    #             skip = (page-1)*limit

    #         data = self.model.get_all(db=db, where_clause=where_clause, skip=skip, limit=limit, sorting_method=sorting_method)

    #         if len(data) < limit:
    #             internal_response_code = 1
    #         else:
    #             internal_response_code = 0

    #         return {"internal_response_code": internal_response_code, "data": data} if data else {"internal_response_code": internal_response_code, "data": data}
    #     except Exception:
    #         raise HTTPException(status_code=500, detail="Something went wrong")

    # async def get_homepage_collection_by_code_and_name(
    #     self,
    #     code: str,
    #     name: str,
    #     db: Session
    # ) -> any:
    #     try:
    #         where_clause = f"""((code='{code}') OR (homepage_collection_name= '{name}')) AND (is_deleted=False)"""
    #         collection = self.model.get_one(db=db, where_clause=where_clause, column_load=HOMEPAGE_COLLECTION_COL_RETURN)

    #         return collection if collection else None
    #     except Exception:
    #         raise HTTPException(status_code=500, detail="Something went wrong")

    # async def get_homepage_collection_by_code(
    #     self,
    #     collection_code: str,
    #     db: Session
    # ) -> any:
    #     try:
    #         where_clause = f"""(code='{collection_code}') AND (is_deleted=False)"""
    #         collection = self.model.get_one(db=db, where_clause=where_clause, column_load=HOMEPAGE_COLLECTION_COL_RETURN)

    #         return collection if collection else None

    #     except Exception:
    #         raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_homepage_collection_by_name(
        self,
        db: Session,
        name: str,
    ) -> any:
        try:
            where_clause = f"""(homepage_collection_name = '{name}') AND (is_deleted = False)"""

            collection = self.model.get_one(db=db, where_clause=where_clause, column_load=HOMEPAGE_COLLECTION_COL_RETURN)

            return collection if collection else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    # async def delete_homepage_collection(
    #     self,
    #     db: Session,
    #     collection_code: str
    # ) -> any:
    #     try:
    #         home_page_collection = await self.get_homepage_collection_by_code(db=db, collection_code=collection_code)
    #         delete_obj = {
    #             "is_deleted": True,
    #             "deleted_at": datetime.now()
    #         }
    #         data = self.model.update(db=db, db_obj=home_page_collection, obj_in=delete_obj)

    #         return {"internal_response_code": 0, "message": "Home Page Collection deleted"} if data else {"internal_response_code": 1, "message": "Home Page Collection not deleted"}
    #     except Exception:
    #         raise HTTPException(status_code=500, detail="Something went wrong")