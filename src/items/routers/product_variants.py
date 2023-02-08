from fastapi import APIRouter, Depends, HTTPException, Security
from auth.authentication_user import get_current_active_user
from items.crud.product_variants import ProductVariantsCollection
from items.models.product_variants import (
    UpdateProductVariantModel,
    CreateProductVariantBaseModel
)
from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()

@router.post(
    "/v1/create_product_variants",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_product_variants(
    product_variants_details: CreateProductVariantBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_variants_collection = ProductVariantsCollection()
        return await product_variants_collection.create_product_variants(db=db, product_variants_details=product_variants_details)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/update_product_variants",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_product_variants(
    product_variants_details: UpdateProductVariantModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_variants_collection = ProductVariantsCollection()
        return await product_variants_collection.update_product_variants(db=db, product_variants_details=product_variants_details)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/get_all_product_variants_by_unique_id",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def get_all_product_variants_by_unique_id(
    unique_id: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_variants_collection = ProductVariantsCollection()
        return await product_variants_collection.get_all_product_variants_by_unique_id(db=db, unique_id=unique_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/delete_sku_code_from_product_variant",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_sku_code_from_product_variant(
    sku_code: str,
    unique_id: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_variants_collection = ProductVariantsCollection()
        return await product_variants_collection.delete_sku_code_from_product_variant(db=db, sku_code=sku_code, unique_id=unique_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")