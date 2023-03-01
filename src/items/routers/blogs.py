from fastapi import APIRouter, Depends, HTTPException, Security
from db.aurora import auroradb
from sqlalchemy.orm import Session
from auth.authentication_user import get_current_active_user
from items.crud.blogs import BlogsCollection
from items.models.blogs import BlogCreateBaseModel, BlogUpdateBaseModel
from typing import List

router = APIRouter()

@router.post(
    "/v1/blog/add_blog",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def add_blog(
    blog: BlogCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        blog_collection = BlogsCollection()
        return await blog_collection.create_blog(blog=blog,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.delete(
    "/v1/blog/delete_blog_by_code",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_blog_by_code(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        blog_collection = BlogsCollection()
        return await blog_collection.delete_blog_by_code(code=code,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/blog/get_blog_by_code",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_blog_by_code(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        blog_collection = BlogsCollection()
        return await blog_collection.get_blog_by_code(code=code,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/blog/get_blogs_by_blog_code_and_name",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_blog_by_blog_code_and_name(
    blog_code: str,
    blog_name: str,
    page_number: int,
    limit: int,
    db: Session = Depends(auroradb.get_db)
):
    try:
        blog_collection = BlogsCollection()
        return await blog_collection.get_blogs_by_blog_code_and_name(blog_name=blog_name,blog_code=blog_code,db=db,page_number=page_number,limit=limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.put(
    "/v1/blog/update_blog",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_blog_media(
    blog: BlogUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        blog_collection = BlogsCollection()
        return await blog_collection.update_blog(blog=blog,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/blog/get_blogs",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_blog_by_code(
    page_number: int,
    limit: int,
    db: Session = Depends(auroradb.get_db)
):
    try:
        blog_collection = BlogsCollection()
        return await blog_collection.get_blogs(page_number=page_number,limit=limit,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/blog/upsert_blogs",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def upsert_blogs(
    blog_details: List[BlogCreateBaseModel],
    db: Session = Depends(auroradb.get_db)
):
    try:
        blog_collection = BlogsCollection()
        return await blog_collection.upsert_multiple_blogs(blog_details=blog_details,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
