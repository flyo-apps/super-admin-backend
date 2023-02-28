from datetime import datetime
from fastapi import HTTPException

from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import exc as orm_exc

from ..models.product_collection import (
    ProductCollectionCreateBaseModel,
    ProductCollectionCreateModel,
    ProductCollectionUpdateBaseModel,
    ProductCollectionUpdateModel
)
from ..schemas.product_collection import (
    ProductCollectionSchema, 
    ProductCollectionItemsSchema
)
from warehouse.schemas.inventory import InventorySchema
from ..schemas.products import ProductsSchema
from ..utils.constants import PRODUCT_COLLECTION_RETURN, PRODUCT_LIMIT, PRODUCT_ITEMS_COL_RETURN

class ProductCollectionCollection:
    def __init__(self):
        self.product_collection_model = CRUDBase(ProductCollectionSchema)
        self.product_collection_items_model = CRUDBase(ProductCollectionItemsSchema)

    async def create_product_collection(
        self,
        product_collection_details: ProductCollectionCreateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{product_collection_details.code}'"""
            existing_product_collection = self.product_collection_model.get_one(db=db, where_clause=where_clause)
            if existing_product_collection is not None:
                return {"internal_response_code": 1, "message": "already exists", "data": None}
            
            product_collection_create = ProductCollectionCreateModel(**product_collection_details.dict())
            
            created_product_collection = self.product_collection_model.create(db=db, obj_in=product_collection_create)

            return {"internal_response_code": 0, "message": "success", "data": None} if created_product_collection else {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_product_collection(
        self,
        product_collection_details: ProductCollectionUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{product_collection_details.code}'"""

            update_values = ProductCollectionUpdateModel(**product_collection_details.dict(exclude_unset=True))
            update_values.is_updated = True
            update_values.updated_at = datetime.now()
            result = self.product_collection_model.filter_update(db=db, where_clause=where_clause, update_values=update_values.dict(exclude_unset=True))
            return {"internal_response_code": 0, "message": "success", "data": None} if result is None else {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def delete_product_collection(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            result = self.product_collection_model.remove(db=db, code=f"""{code}""")
            if result:
                where_clause = f"""collection_code='{code}'"""
                result_2 = self.product_collection_items_model.remove(db=db, where_clause=where_clause)
            return {"internal_response_code": 0, "message": "success", "data": None} if result and not result_2 else {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception as e:
            if type(e) == orm_exc.UnmappedInstanceError:
                return {"internal_response_code": 11, "message": "entity does not exist", "data": None}
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def add_element_to_collection(
        self,
        sku_code: str,
        collection_name: str,
        code: str,
        sort_priority: int,
        db: Session
    ) -> any:
        try:
            item_to_add = {
                "code": f"""{code}_{sku_code}""",
                "sku_code": sku_code,
                "collection_code": code,
                "collection_name": collection_name,
                "sort_priority": sort_priority
            }
            result = self.product_collection_items_model.create(db=db, obj_in=item_to_add)
            return {"internal_response_code": 0, "message": "success", "data": None} if result  else {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def remove_element_from_collection(
        self,
        sku_code: str,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""collection_code='{code}' AND sku_code='{sku_code}'"""
            result = self.product_collection_items_model.remove(db=db, where_clause=where_clause)
            return {"internal_response_code": 0, "message": "success", "data": None} if not result  else {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_product_collection_by_code(
        self,
        code: str,
        page: int,
        db: Session
    ) -> any:
        try:
            if page == 1:
                skip = 0
            else:
                skip = (page-1)*PRODUCT_LIMIT

            where_clause = f"""collection_code='{code}' and inventory.qty>0 and products.sort_priority1>0 and products.live='true'"""
            sorting_clause = f"""sort_priority desc"""

            product_collection = self.product_collection_items_model.get_all_with_multiple_join_and_sorting_and_both_load(
                db=db, 
                where_clause=where_clause, 
                join_model=ProductsSchema, 
                join_model_1=InventorySchema,
                column_load_1=PRODUCT_COLLECTION_RETURN, 
                column_load_2= PRODUCT_ITEMS_COL_RETURN,
                sorting_method=sorting_clause,
                skip=skip,
                limit=PRODUCT_LIMIT
            )

            data_to_return = {
                "product_collection_data": {},
                "products": []
            }

            for index, value in enumerate(product_collection):
                if index == 0:
                    data_to_return["product_collection_data"] = {
                        "collection_name": value["ProductCollectionItemsSchema"].collection_name,
                        "code": value["ProductCollectionItemsSchema"].collection_code,
                    }
                data_to_return["products"].append(value["ProductsSchema"].__dict__)
            
            if len(data_to_return["products"]) < PRODUCT_LIMIT:
                internal_response_code = 1
            else:
                internal_response_code = 0

            return {"internal_response_code": internal_response_code, "message": "success", "data": data_to_return} if product_collection else {"internal_response_code": 2, "message": "failed", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_collection_detail_by_code(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            collection_detail = self.product_collection_model.get_one(db=db, code=code)
            return collection_detail if collection_detail else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_all_collection_items_by_code(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = where_clause = f"""collection_code='{code}'"""
            result = self.product_collection_items_model.get_all(db=db, where_clause=where_clause,skip=0,limit=1000)
            data_to_return = {}
            for i in result:
                data_to_return[f"""{i.__dict__["sku_code"]}"""] = f"""{i.__dict__["sort_priority"]}"""

            return data_to_return if result else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
