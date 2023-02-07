from fastapi import APIRouter, Depends, HTTPException, Security
from db.aurora import auroradb
from sqlalchemy.orm import Session
from auth.authentication_user import get_current_active_user
from items.crud.shipping_data import ShippingDataCollection
from items.models.shipping_data import ShippingDataCreateBaseModel, ShippingDataUpdateBaseModel
from typing import List
from pydantic import constr

router = APIRouter()

@router.post(
    "/v1/add_shipping_detail",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def add_shipping_detail(
    shipping_details: ShippingDataCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        shipping_collection = ShippingDataCollection()
        return await shipping_collection.create_shipping_data(shipping_details=shipping_details,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.delete(
    "/v1/delete_shipping_detail",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_shipping_detail(
    code: constr(to_lower=True),
    db: Session = Depends(auroradb.get_db)
):
    try:
        shipping_collection = ShippingDataCollection()
        return await shipping_collection.delete_shipping_data(code=code,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/get_shipping_detail",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_shipping_detail(
    code: constr(to_lower=True),
    db: Session = Depends(auroradb.get_db)
):
    try:
        shipping_collection = ShippingDataCollection()
        return await shipping_collection.get_shipping_details(code=code,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.put(
    "/v1/update_shipping_detail",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_shipping_detail(
    shipping_details: ShippingDataUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        shipping_collection = ShippingDataCollection()
        return await shipping_collection.update_shipping_details(shipping_details=shipping_details,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/upsert_multiple_shipping_details",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def upsert_multiple_shipping_details(
    shipping_details: List[ShippingDataCreateBaseModel],
    db: Session = Depends(auroradb.get_db)
):
    try:
        shipping_collection = ShippingDataCollection()
        return await shipping_collection.upsert_multiple_shipping_data(shipping_details=shipping_details,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
