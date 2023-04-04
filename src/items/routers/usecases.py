from fastapi import APIRouter, Depends, HTTPException, Security
from auth.authentication_user import get_current_active_user
from ..crud.usecases import UsecaseCollection
from ..models.usecases import (
    UsecaseCreateBaseModel,
    UsecaseUpdateBaseModel
)
from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/v1/create_usecase",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_usecase(
    usecase_details: UsecaseCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        usecase_collection = UsecaseCollection()
        return await usecase_collection.create_usecase(usecase_details=usecase_details,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/update_usecase",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_usecase(
    usecase_update_details: UsecaseUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        usecase_collection = UsecaseCollection()
        return await usecase_collection.update_usecase(usecase_update_details=usecase_update_details,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/delete_usecase",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_usecase(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        usecase_collection = UsecaseCollection()
        return await usecase_collection.delete_usecase(code=code,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/get_usecase",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_usecase(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        usecase_collection = UsecaseCollection()
        return await usecase_collection.get_usecase(code=code,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")