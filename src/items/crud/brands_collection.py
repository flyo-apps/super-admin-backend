from datetime import datetime
import copy
from fastapi import HTTPException
from ..utils.constants import BRANDS_COLLECTION_COL_RETURN
from ..models.brands_collection import (
    BrandsCollectionCreateBaseModel,
    BrandsCollectionCreateModel,
    BrandsCollectionUpdateBaseModel,
    BrandsCollectionUpdateModel,
    BrandsCollectionDeleteModel
)
from ..schemas.brands_collection import (
    BrandsCollectionSchema
)

from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session

class BrandsCollectionCollection:
    def __init__(self):
        self.model = CRUDBase(BrandsCollectionSchema)

    async def create_brand_collection(
        self,
        brands_collection_details: BrandsCollectionCreateBaseModel,
        db: Session
    ) -> any:
        try:
            existing_brands_collection = self.model.get_one(db=db, code=brands_collection_details.code)
            if existing_brands_collection is not None:
                return

            brands_collection_create = BrandsCollectionCreateModel(**brands_collection_details.dict())
            created_brands_collection = self.model.create(db=db, obj_in=brands_collection_create)

            return created_brands_collection if created_brands_collection else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def update_brands_collection(
        self,
        brands_collection_update_details: BrandsCollectionUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            usecase = self.model.get_one(db=db, code=brands_collection_update_details.code)
            if usecase == None:
                return {"internal_response_code": 1, "code": brands_collection_update_details.code, "message": "Usecase not found"}

            brands_collection_update = BrandsCollectionUpdateModel(**brands_collection_update_details.dict(exclude_unset=True))
            brands_collection_update.is_updated = True
            brands_collection_update.updated_at = datetime.now()
            updated_brands_collection = self.model.update(db=db, db_obj=usecase,obj_in=brands_collection_update)
            return {"internal_response_code": 0, "code": brands_collection_update_details.code, "message": "Brands Collection updated"} if updated_brands_collection else {"internal_response_code": 1, "code": brands_collection_update_details.code, "message": "Brands Collection not updated"}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def delete_brands_collection(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            brands_collection_delete = BrandsCollectionDeleteModel(code=code)
            brands_collection_delete_dict = brands_collection_delete.dict()
            brands_collection = self.model.get_one(db=db, code=code)
            if brands_collection == None:
                {"internal_response_code": 1, "code": code, "message": "Brands Collection not found"}
            deleted_usecase = self.model.update(db=db, db_obj=brands_collection,obj_in=brands_collection_delete_dict)

            return {"internal_response_code": 0, "code": code, "message": "Brands Collection deleted"} if deleted_usecase else {"internal_response_code": 1, "code": code, "message": "Brands Collection not deleted"} 
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def get_brand_collection_by_code(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            brands_collection = self.model.get_one(db=db, code=code, column_load=BRANDS_COLLECTION_COL_RETURN)

            return brands_collection if brands_collection else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def get_brand_collection_by_name(
        self,
        name: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""(brand_collection_name= '{name}') AND (is_deleted=False)"""
            brands_collection = self.model.get_one(db=db, where_clause=where_clause, column_load=BRANDS_COLLECTION_COL_RETURN)

            return brands_collection if brands_collection else None
        except Exception:

            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_all_brands_collection(
        self,
        page: int,
        limit: int,
        db: Session
    ) -> any:
        try:
            if page == 1:
                skip = 0
            else:
                skip = (page - 1)*limit
        
            where_clause = "(is_deleted=False)"
            data = self.model.get_all(db=db, column_load=BRANDS_COLLECTION_COL_RETURN, where_clause=where_clause, skip=skip, limit=limit)

            return data if data else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    
    async def add_homepage_component_to_brand_collection(
        self,
        db: Session,
        code: str,
        rank: int,
        homepage_component_data: dict
    ) -> any:
        try:
            del homepage_component_data['_sa_instance_state']
            brand_collection_details = await self.get_brand_collection_by_code(code=code, db=db)
            if brand_collection_details == None:
                return {"internal_response_code": 1, "message": "Brand not found", "data": None}
            

            items_list = brand_collection_details.items_list
            homepage_component_values_list = []
            homepage_component_values_list.append(homepage_component_data)
            homepage_component = {
                "name": "Homepage Component",
                "values": homepage_component_values_list,
                "type": "homepage_component",
                "rank": rank
            }
            
            if items_list == None:
                items_list = []

            if len(items_list) < rank:
                items_list.append(homepage_component)
            else:
                items_list.insert(rank, homepage_component)

            where_clause = f"""code='{code}'"""
            update_values = {
                "items_list": copy.deepcopy(items_list)
            }

            updated = self.model.filter_update(db=db, where_clause=where_clause, update_values=update_values)

            return {"internal_response_code": 0, "message": "added", "data": update_values["items_list"]} if updated is None else {"internal_response_code": 1, "message": "Something went wrong while updating", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    
    async def remove_homepage_component_from_brand_collection(
        self,
        db: Session,
        code: str,
        homepage_component_data: dict
    ) -> any:
        try:
            del homepage_component_data['_sa_instance_state']
            brand_collection_details = await self.get_brand_collection_by_code(code=code, db=db)
            if brand_collection_details == None:
                return {"internal_response_code": 1, "message": "Brand not found", "data": None}
            
            
            items_list = brand_collection_details.items_list

            if items_list == None:
                return {"internal_response_code": 1, "message": "Item list is empty", "data": None}
            if len(items_list) <= 0:
                return {"internal_response_code": 1, "message": "Item list is empty", "data": None}

            indexes = [index for index,value in enumerate(items_list) if (value != [] and value["type"] == 'homepage_component' and value["values"][0]["component_title"]==homepage_component_data["component_title"] and value["values"][0]["homepage_name"]==homepage_component_data["homepage_name"]) ]
            if len(indexes) <= 0:
                return {"internal_response_code": 1, "message": "Homepage Component not found", "data": None}
            
            items_list.pop(indexes[0])

            where_clause = f"""code='{code}'"""
            update_values = {
                "items_list": copy.deepcopy(items_list)
            }

            updated = self.model.filter_update(db=db, where_clause=where_clause, update_values=update_values)

            return {"internal_response_code": 0, "message": "removed", "data": update_values["items_list"]} if updated is None else {"internal_response_code": 1, "message": "Something went wrong while updating", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")