from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List
from auth.authentication_user import get_current_active_user
from ..crud.products import ProductsCollection
from ..models.products import (
    ProductCreateBaseModel,
    ProductUpdateBaseModel,
    ProductUpdateDescriptionBaseModel,
    ProductUpdateSeoBaseModel,
    ProductUpdateStateBaseModel,
)
from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/v1/create_product",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_product(
    products_details: ProductCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.create_product(products_details=products_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/upsert_products",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def upsert_products(
    products_details: List[Union[ProductCreateBaseModel, ProductUpdateBaseModel]],
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.upsert_multiple_products(products_details=products_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/update_product",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_product(
    product_update_details: ProductUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.update_product(product_update_details=product_update_details, db=db)

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.put(
    "/v1/bulk_update_products",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def bulk_update_products(
    product_update_details: List[ProductUpdateBaseModel],
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.bulk_update_products(product_update_details=product_update_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/update_product_state",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_product_state(
    product_update_state_details: ProductUpdateStateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.update_product_state(
            product_update_state_details=product_update_state_details,
            db=db
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/update_multiple_products_state",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_multiple_products_state(
    products_update_state_details: List[ProductUpdateStateBaseModel],
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.bulk_update_products_state(
            products_update_state_details=products_update_state_details,
            db=db
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/update_product_desc",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_product_desc(
    product_update_description_details: ProductUpdateDescriptionBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.update_product_desc(
            product_update_description_details=product_update_description_details,
            db=db
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/update_multiple_products_desc",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_multiple_products_desc(
    products_update_description_details: List[ProductUpdateDescriptionBaseModel],
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.bulk_update_products_desc(
            products_update_description_details=products_update_description_details,
            db=db
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/update_product_seo",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_product_seo(
    product_update_seo_details: ProductUpdateSeoBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.update_product_seo(
            product_update_seo_details=product_update_seo_details,
            db=db
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/products/get_product_by_sku_code",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_product_by_sku_code(
    sku_code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.get_product_by_sku_code(sku_code=sku_code, db=db, products_mapping=True)

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/products/delete_product",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_product(
    sku_code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        products_collection = ProductsCollection()

        return await products_collection.delete_product(
            sku_code=sku_code,
            db=db
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/get_products_by_sku_codes",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_products_by_sku_codes(
    sku_codes: List[str],
    db: Session = Depends(auroradb.get_db),
):
    try:
        products_collection = ProductsCollection()
        products_list =  await products_collection.get_products_by_sku_codes(db=db,sku_codes=sku_codes)

        return {"internal_response_code": 0, "message": "success", "data": products_list} if products_list else {"internal_response_code": 1, "message": "failed", "data": None} 
    except Exception:
        raise HTTPException(status_code=500, details="Something went wrong")