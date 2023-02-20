from sqlalchemy.orm import exc as orm_exc
from fastapi import HTTPException
from items.schemas.product_variants import ProductVariantsSchema, ProductVariantsMapSchema
from items.models.product_variants import (
    CreateProductVariantBaseModel,
    CreateProductVariantModel,
    CreateProductVariantMapModel
)
from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session

class ProductVariantsCollection:
    def __init__(self):
        self.product_variants_model = CRUDBase(ProductVariantsSchema)
        self.product_variants_map_model = CRUDBase(ProductVariantsMapSchema)

    async def create_product_variants(
        self,
        product_variants_details: CreateProductVariantBaseModel,
        db: Session
    ) -> any:
        try:
            product_variants_create_details = CreateProductVariantModel(
                **product_variants_details.dict(), 
                code=f"""{product_variants_details.sku_code}_{product_variants_details.unique_id}"""
            )
            product_variants_map_create_details = CreateProductVariantMapModel(
                code=f"""{product_variants_details.sku_code}_{product_variants_details.unique_id}""",
                sku_code=product_variants_details.sku_code,
                unique_id=product_variants_details.unique_id
            )

            created_product_variants_map = self.product_variants_map_model.create(db=db, obj_in=product_variants_map_create_details)
            if created_product_variants_map == None:
                return {"internal_response_code": 1, "message": "Something went wrong", "data": None}

            created_product_variants = self.product_variants_model.create(db=db, obj_in=product_variants_create_details)
            
            return {"internal_response_code": 0, "message": "Product variants added", "data": None} if created_product_variants else {"internal_response_code": 1, "message": "Product variants not added", "data": None}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    

    async def update_product_variants(
        self,
        product_variants_details: CreateProductVariantModel,
        db: Session
    ) -> any:
        try:
            product_variant = self.product_variants_model.get_one(db=db, code=f"""{product_variants_details.sku_code}_{product_variants_details.unique_id}""")
            if product_variant == None:
                return {"internal_response_code": 1, "message": "No product variants exists with this details", "data": None}

            updated_product_variants = self.product_variants_model.update(db=db, db_obj=product_variant ,obj_in=product_variants_details.dict(exclude_unset=True))
            
            return {"internal_response_code": 0, "message": "Product variants updated", "data": None} if updated_product_variants else {"internal_response_code": 1, "message": "Product variants not updated", "data": None}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def get_all_product_variants_by_unique_id(
        self,
        unique_id: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""unique_id='{unique_id}'"""
            product_variants = self.product_variants_model.get_all(db=db, where_clause=where_clause)
            return {"internal_response_code": 0, "message": "Success", "data": product_variants} if product_variants else {"internal_response_code": 1, "message": "Failure", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def delete_sku_code_from_product_variant(
        self,
        sku_code: str,
        unique_id: str,
        db: Session
    ) -> any:
        try:
            self.product_variants_map_model.remove(db=db, code=f"""{sku_code}_{unique_id}""")
            self.product_variants_model.remove(db=db, code=f"""{sku_code}_{unique_id}""")

            return {"internal_response_code": 0, "message": "Success", "data": None}
        except Exception as e:
            if type(e) == orm_exc.UnmappedInstanceError:
                return {"internal_response_code": 1, "message": "Product does not exists in Product Variants"}
            raise HTTPException(status_code=500, detail="Something went wrong")