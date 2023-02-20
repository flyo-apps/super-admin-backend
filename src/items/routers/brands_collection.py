from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from auth.authentication_user import get_current_active_user
from ..crud.brands_collection import BrandsCollectionCollection
from ..models.brands_collection import (
    BrandsCollectionCreateBaseModel,
    BrandsCollectionUpdateBaseModel
)
from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/v1/create_brand_collection",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_brand_collection(
    brands_collection_details: BrandsCollectionCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        brands_collection_collection = BrandsCollectionCollection()
        return await brands_collection_collection.create_brand_collection(brands_collection_details=brands_collection_details,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/update_brands_collection",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_brands_collection(
    brands_collection_update_details: BrandsCollectionUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        brands_collection_collection = BrandsCollectionCollection()
        return await brands_collection_collection.update_brands_collection(brands_collection_update_details=brands_collection_update_details,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/delete_brands_collection",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_brands_collection(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        brands_collection_collection = BrandsCollectionCollection()
        return await brands_collection_collection.delete_brands_collection(code=code,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/get_brands_collection",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_brand_collection_by_code(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        brands_collection_collection = BrandsCollectionCollection()
        return await brands_collection_collection.get_brand_collection_by_code(code=code,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

#not used in admin panel scripts
@router.post(
    "/v1/get_all_brands_collection",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_all_brand_collection(
    db: Session = Depends(auroradb.get_db),
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
):
    try:
        brands_collection_collection = BrandsCollectionCollection()
        return await brands_collection_collection.get_all_brands_collection(limit=limit, db=db, page=page)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")