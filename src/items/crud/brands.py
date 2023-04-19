import copy
from datetime import datetime
from fastapi import HTTPException
from .categories import CategoriesCollection
from ..models.brands import (
    BrandCreateModel,
    BrandCreateBaseModel,
    BrandUpdateModel,
    BrandUpdateBaseModel,
    BrandDeleteModel
)
from ..schemas.brands import (
    BrandsSchema
)
from ..utils.constants import (
    BRANDS_COL_RETURN
)
from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session

class BrandsCollection:
    def __init__(self):
        self.model = CRUDBase(BrandsSchema)

    async def create_brand(
        self,
        brand_details: BrandCreateBaseModel,
        db: Session
    ) -> any:
        try:
            existing_brand = self.model.get_one(db=db, code=brand_details.code)
            if existing_brand is not None:
                return

            brand_create = BrandCreateModel(**brand_details.dict())
            created_brand = self.model.create(db=db, obj_in=brand_create)

            return created_brand if created_brand else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def update_brand(
        self,
        brand_update_details: BrandUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            brand = self.model.get_one(db=db, code=brand_update_details.code)
            if brand == None:
                return {"internal_response_code": 1, "brand_code": brand_update_details.code, "message": "Brand not found"}

            brand_update = BrandUpdateModel(**brand_update_details.dict(exclude_unset=True))
            brand_update.is_updated = True
            brand_update.updated_at = datetime.now()
            updated_brand = self.model.update(db=db, db_obj=brand,obj_in=brand_update)

            return {"internal_response_code": 0, "brand_code": brand_update_details.code, "message": "Brand updated"} if updated_brand else {"internal_response_code": 1, "brand_code": brand_update_details.code, "message": "Brand not updated"}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_all_brands(
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

            data = self.model.get_all(db=db, column_load=BRANDS_COL_RETURN, where_clause=where_clause, skip=skip, limit=limit)

            return data if data else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_brand(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            brand = self.model.get_one(db=db, code=code, column_load=BRANDS_COL_RETURN)

            return brand if brand else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def remove_from_all_categories(
        self,
        brand_title: str
    ) -> any:
        try:
            brand_details = await self.get_brand_by_title(brand_title=brand_title)

            if brand_details is not None and brand_details.categories is not None:
                categories_collection = CategoriesCollection()
                
                for category_id in brand_details.categories:
                    await categories_collection.remove_brand_from_category_id(category_id=category_id, brand_id=brand_details.id)
    
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_list_item_type(
        self,
        list_name: str
    ) -> any:
        try:
            if list_name == "top_products":
                return "product"
            elif list_name == "new_products":
                return "product"
            elif list_name == "trending_products":
                return "product"
            elif list_name == "discounted_products":
                return "product"
            elif list_name == "product_types":
                return "product_type"
            elif list_name == "subcategories":
                return "category"
            elif list_name == "categories":
                return "category"
            elif list_name == "filters":
                return "filter"
            elif list_name == "images":
                return "image"
            else:
                return None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def delete_brand(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            brand_delete = BrandDeleteModel(code=code)
            brand_delete_dict = brand_delete.dict()
            brand = self.model.get_one(db=db, code=code)
            if brand == None:
                {"internal_response_code": 1, "code": code, "message": "Brand not found"}
            deleted_brand = self.model.update(db=db, db_obj=brand,obj_in=brand_delete_dict)

            return {"internal_response_code": 0, "code": code, "message": "Brand deleted"} if deleted_brand else {"internal_response_code": 1, "code": code, "message": "Brand not deleted"} 
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def create_brand_store(
       self,
       brand_name: str,
       db: Session
    ) -> any:
        try:
            query = f"""select * from brand_store('{brand_name}', 'create')"""
            updated = self.model.call_postgres_function(db=db, query=query)
            return {"internal_response_code": 0, "message": "success", "data": None} if updated[0][0] else {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def remove_brand_store(
        self,
        brand_name: str,
        db: Session
    ) -> any:
        try:
            query = f"""select * from brand_store('{brand_name}', 'remove')"""
            updated = self.model.call_postgres_function(db=db, query=query)
            return {"internal_response_code": 0, "message": "success", "data": None} if updated else {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    
    async def add_homepage_component_to_brand(
        self,
        db: Session,
        code: str,
        rank: int,
        homepage_component_data: dict
    ) -> any:
        try:
            del homepage_component_data['_sa_instance_state']
            brand_details = await self.get_brand(code=code, db=db)
            if brand_details == None:
                return {"internal_response_code": 1, "message": "Brand not found", "data": None}
            

            items_list = brand_details.items_list
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

    
    async def remove_homepage_component_from_brand(
        self,
        db: Session,
        code: str,
        homepage_component_data: dict
    ) -> any:
        try:
            del homepage_component_data['_sa_instance_state']
            brand_details = await self.get_brand(code=code, db=db)
            if brand_details == None:
                return {"internal_response_code": 1, "message": "Brand not found", "data": None}
            

            items_list = brand_details.items_list
            if items_list == None:
                return {"internal_response_code": 1, "message": "Item list is empty", "data": None}
            if len(items_list) <= 0:
                return {"internal_response_code": 1, "message": "Item list is empty", "data": None}
                
            indexes = [index for index,value in enumerate(items_list) if (value["type"] == 'homepage_component' and value["values"][0]["component_title"]==homepage_component_data["component_title"] and value["values"][0]["homepage_name"]==homepage_component_data["homepage_name"]) ]
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