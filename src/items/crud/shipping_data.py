from items.models.shipping_data import ShippingDataCreateBaseModel, ShippingDataCreateModel,ShippingDataDeleteModel, ShippingDataUpdateBaseModel, ShippingDataUpdateModel
from ..schemas.shipping_data import ShippingDataSchema
from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

class ShippingDataCollection:
    def __init__(self):
        self.model = CRUDBase(ShippingDataSchema)
    
    async def create_shipping_data(
        self,
        shipping_details: ShippingDataCreateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""(code='{shipping_details.code}') AND is_deleted=false"""
            existing_shipping_data = self.model.get_one(db=db, where_clause=where_clause)
            if existing_shipping_data is not None:
                return {"internal_response_code": 1, "message": f"""code {shipping_details.code} already exists"""}

            shipping_details_create = ShippingDataCreateModel(**shipping_details.dict())
            created_shipping_details = self.model.create(db=db, obj_in=shipping_details_create)

            return {"internal_response_code": 0, "message": f"""shippind details for code {shipping_details.code} created"""} if created_shipping_details else {"internal_response_code": 1, "message": f"""failed to created shippind details for code {shipping_details.code}"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def delete_shipping_data(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{code}'  AND is_deleted=false"""
            existing_shipping_data = self.model.get_one(db=db, where_clause=where_clause)
            if existing_shipping_data is None:
                return {"internal_response_code": 1, "message": f"""code {code} not found"""}

            shipping_data_delete_dict = ShippingDataDeleteModel(code=code).dict()
            deleted_shipping_data = self.model.update(db=db, db_obj=existing_shipping_data, obj_in=shipping_data_delete_dict)

            return {"internal_response_code": 0, "message": f"""shipping details for code {code} deleted"""} if deleted_shipping_data else {"internal_response_code": 1, "message": f"""failed to delete shipping details for code {code}"""} 
 
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_shipping_details(
        self,
        shipping_details: ShippingDataUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""(code='{shipping_details.code}' AND is_deleted=false)"""
            existing_shipping_data = self.model.get_one(db=db, where_clause=where_clause)
            if existing_shipping_data is None:
                return {"internal_response_code": 1, "message": f"""code {shipping_details.code} not found"""}

            shipping_details_update = ShippingDataUpdateModel(**shipping_details.dict())
            updated_shipping_data = self.model.update(db=db, db_obj=existing_shipping_data, obj_in=shipping_details_update)

            return {"internal_response_code": 0, "message": f"""shipping details for code  {shipping_details.code} updated"""} if updated_shipping_data else {"internal_response_code": 1, "message": f"""failed to update shipping details for code {shipping_details.code}"""}
        except:
           raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_shipping_details(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""(code='{code.lower()}' AND is_deleted=false)"""
            existing_shipping_data = self.model.get_one(db=db, where_clause=where_clause)

            return {"internal_response_code": 0, "data": existing_shipping_data} if existing_shipping_data else {"internal_response_code": 1, "message": f"""shipping details for code {code} not found"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def upsert_multiple_shipping_data(
        self,
        shipping_details: List[ShippingDataCreateBaseModel],
        db: Session
    ) -> any:
        try:
            codes = ','.join(["'" + data.code + "'" for data in shipping_details])
            existing_codes = []
            where_clause = f"""code IN ({codes})"""
            existing_shipping_data = self.model.get_all(db=db, where_clause=where_clause,skip=0,limit=len(shipping_details))
            if existing_shipping_data:
                existing_codes = [data.code for data in existing_shipping_data]

            shipping_details_create = []
            shipping_details_update = []
            for shipping_data in shipping_details:
                if shipping_data.code not in existing_codes:
                    shipping_data_create = ShippingDataCreateModel(**shipping_data.dict())
                    shipping_details_create.append(shipping_data_create.dict())
                else:
                    shipping_data_update = ShippingDataUpdateModel(**shipping_data.dict())
                    shipping_details_update.append(shipping_data_update.dict())

            res = self.model.bulk_upsert(db=db, update_vals=shipping_details_update,insert_vals=shipping_details_create)
            return {"internal_response_code": 0, "message": f"""shippind details created for {len(shipping_details_create)} codes and updated for {len(shipping_details_update)} codes"""} if res is None else {"internal_response_code": 1, "message": f"""upsert operation failed"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")