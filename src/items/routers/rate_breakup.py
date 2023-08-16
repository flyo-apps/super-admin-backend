from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Security
from auth.authentication_user import get_current_active_user

from items.crud.rate_breakup import RateBreakupCollection
from items.models.rate_breakup import RateBreakupCreateBaseModel, RateBreakupUpdateBaseModel

from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/v1/create_rate_breakup",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_rate_breakup(
    create_rate_breakup: RateBreakupCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        rate_breakup_collection = RateBreakupCollection()
        return await rate_breakup_collection.create_rate_breakup(create_rate_breakup=create_rate_breakup.dict(), db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/update_rate_breakup",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_rate_breakup(
    update_rate_breakup: RateBreakupUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        rate_breakup_collection = RateBreakupCollection()
        return await rate_breakup_collection.update_rate_breakup(update_rate_breakup=update_rate_breakup.dict(exclude_unset=True), db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/get_rate_breakup_by_code",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_rate_breakup_by_code(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        rate_breakup_collection = RateBreakupCollection()
        return await rate_breakup_collection.get_rate_breakup_by_code(code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/delete_rate_breakup_by_code",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_rate_breakup_by_code(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        rate_breakup_collection = RateBreakupCollection()
        return await rate_breakup_collection.delete_rate_breakup_by_code(code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/get_all_rate_breakup",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_all_rate_breakup(
    db: Session = Depends(auroradb.get_db)
):
    try:
        rate_breakup_collection = RateBreakupCollection()
        return await rate_breakup_collection.get_all_rate_breakup(db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/get_all_rate_breakup_by_brand_and_or_metal",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_all_rate_breakup_by_brand_and_or_metal(
    db: Session = Depends(auroradb.get_db),
    brand: Optional[str] = None,
    metal: Optional[str] = None,
):
    try:
        if brand == None and metal == None:
            return {"internal_response_code": 1, "message": "Either provide metal or brand or both", "data": None}
        rate_breakup_collection = RateBreakupCollection()
        return await rate_breakup_collection.get_all_rate_breakup_by_brand_and_or_metal(db=db, brand=brand, metal=metal)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")