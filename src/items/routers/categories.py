
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from auth.authentication_user import get_current_active_user
from ..crud.categories import CategoriesCollection
from ..models.categories import (
    CategoryCreateBaseModel,
    CategoryUpdateBaseModel
)

from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/v1/create_category",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_category(
    category_details: CategoryCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.create_category(category_details=category_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/update_category",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_category(
    category_update_details: CategoryUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.update_category(category_update_details=category_update_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/v1/get_all_categories",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_all_categories(
    db: Session = Depends(auroradb.get_db),
    page: Optional[int] = 1,
    limit: Optional[int] = 30,
):
    try:
        categories_collection = CategoriesCollection()
        return await categories_collection.get_all_categories(db=db, limit=limit, page=page)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/v1/get_all_categories_lists",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_all_categories_lists(
    parent_category: Optional[str] = None
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.get_all_categories_lists()

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/v1/get_category",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_category(
    category_code: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.get_category(db=db, category_code=category_code)

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/delete_category",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_category(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.delete_category(code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/disable_category",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def disable_category(
    category_id: str
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.disable_category(
            category_id=category_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/v1/search_category",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def search_category(
    search_keyword: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.search_category(db=db, search_keyword = search_keyword)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
