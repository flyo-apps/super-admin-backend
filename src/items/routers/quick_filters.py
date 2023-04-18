from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Security
from auth.authentication_user import get_current_active_user

from items.crud.quick_filters import QuickFiltersCollection

from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/v1/create_quick_filters",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_quick_filters(
    screen_filter: dict,
    data: List[dict],
    db: Session = Depends(auroradb.get_db)
):
    try:
        quick_filters_collection = QuickFiltersCollection()
        return await quick_filters_collection.create_quick_filters(screen_filter=screen_filter, data=data, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
    
@router.post(
    "/v1/update_quick_filters",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_quick_filters(
    screen_filter: dict,
    data: List[dict],
    db: Session = Depends(auroradb.get_db)
):
    try:
        quick_filters_collection = QuickFiltersCollection()
        return await quick_filters_collection.update_quick_filters(screen_filter=screen_filter, data=data, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/get_quick_filters",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_quick_filters(
    screen_filter: dict,
    db: Session = Depends(auroradb.get_db)
):
    try:
        quick_filters_collection = QuickFiltersCollection()
        return await quick_filters_collection.get_quick_filters(screen_filter=screen_filter, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/delete_quick_filters",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def delete_quick_filters(
    screen_filter: dict,
    db: Session = Depends(auroradb.get_db)
):
    try:
        quick_filters_collection = QuickFiltersCollection()
        return await quick_filters_collection.delete_quick_filters(screen_filter=screen_filter, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

