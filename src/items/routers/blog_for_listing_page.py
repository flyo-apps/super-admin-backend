from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Security
from auth.authentication_user import get_current_active_user

from items.crud.blog_for_listing_page import BlogForListingPageCollection
from items.models.blog_for_listing_page import BlogForListPageCreateBaseModel, BlogForListPageUpdateBaseModel

from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/v1/create_blog_for_listing_page",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_blog_for_listing_page(
    data: BlogForListPageCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        blog_for_listing_page_collection = BlogForListingPageCollection()
        return await blog_for_listing_page_collection.create_blog_for_listing_page(data=data, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
    
@router.post(
    "/v1/update_blog_for_listing_page",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_blog_for_listing_page(
    data: BlogForListPageUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        blog_for_listing_page_collection = BlogForListingPageCollection()
        return await blog_for_listing_page_collection.update_blog_for_listing_page(data=data, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/get_blog_for_listing_page",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_blog_for_listing_page(
    screen_filter: Optional[dict] = None,
    code: Optional[str] = None,
    db: Session = Depends(auroradb.get_db)
):
    try:
        if (screen_filter == None and code == None) or (screen_filter != None and code != None):
            return {"internal_response_code": 1,  "message": "Either send code or screen_filter", "data": None}

        blog_for_listing_page_collection = BlogForListingPageCollection()
        return await blog_for_listing_page_collection.get_blog_for_listing_page(screen_filter=screen_filter, code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/delete_blog_for_listing_page",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_blog_for_listing_page(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        blog_for_listing_page_collection = BlogForListingPageCollection()
        return await blog_for_listing_page_collection.delete_blog_for_listing_page(code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

