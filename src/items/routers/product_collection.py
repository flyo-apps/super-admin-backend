from fastapi import APIRouter, Depends, HTTPException, Security
from auth.authentication_user import get_current_active_user
from ..crud.product_collection import ProductCollectionCollection
from ..models.product_collection import (
    ProductCollectionCreateBaseModel,
    ProductCollectionUpdateBaseModel
)
from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()

@router.post(
    "/v1/create_product_collection",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_product_collection(
    product_collection_details: ProductCollectionCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_collection_collection = ProductCollectionCollection()
        return await product_collection_collection.create_product_collection(db=db, product_collection_details=product_collection_details)

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/update_product_collection",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_product_collection(
    product_collection_details:  ProductCollectionUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_collection_collection = ProductCollectionCollection()
        return await product_collection_collection.update_product_collection(
            db=db, 
            product_collection_details=product_collection_details
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/delete_product_collection",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_product_collection(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_collection_collection = ProductCollectionCollection()
        return await product_collection_collection.delete_product_collection(db=db, code=code)

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/add_element_to_collection",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def add_element_to_collection(
    sku_code: str,
    collection_name: str,
    code: str,
    sort_priority: int,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_collection_collection = ProductCollectionCollection()
        return await product_collection_collection.add_element_to_collection(
            db=db, 
            code=code, 
            sku_code=sku_code,
            collection_name=collection_name,
            sort_priority=sort_priority
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/remove_element_from_collection",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def remove_element_from_collection(
    sku_code: str,
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_collection_collection = ProductCollectionCollection()
        return await product_collection_collection.remove_element_from_collection(
            db=db, 
            code=code, 
            sku_code=sku_code,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/get_product_collection_by_code",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_product_collection_by_code(
    code: str,
    page: int = 1,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_collection_collection = ProductCollectionCollection()
        return await product_collection_collection.get_product_collection_by_code(db=db, code=code, page=page)

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/get_collection_detail_by_code",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_collection_detail_by_code(
    code:str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_collection_collection = ProductCollectionCollection()
        return await product_collection_collection.get_collection_detail_by_code(db=db, code=code)

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/get_all_collection_items_by_code",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_collection_detail_by_code(
    code:str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_collection_collection = ProductCollectionCollection()
        return await product_collection_collection.get_all_collection_items_by_code(db=db, code=code)

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")