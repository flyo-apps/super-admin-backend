from fastapi import APIRouter, Depends, HTTPException, Security
from db.aurora import auroradb
from sqlalchemy.orm import Session
from auth.authentication_user import get_current_active_user
from items.crud.product_reviews import ProductReviewsCollection
from items.models.product_reviews import ProductReviewCreateBaseModel, ProductReviewUpdateBaseModel
from typing import List

router = APIRouter()

@router.post(
    "/v1/add_review",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def add_review(
    review: ProductReviewCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_reviews_collection = ProductReviewsCollection()
        return await product_reviews_collection.add_review(review=review,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.put(
    "/v1/update_review",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_review(
    review: ProductReviewUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_reviews_collection = ProductReviewsCollection()
        return await product_reviews_collection.update_review(review=review,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.delete(
    "/v1/delete_review",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_review(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_reviews_collection = ProductReviewsCollection()
        return await product_reviews_collection.delete_review(code=code,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/get_review_by_code",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_review_by_code(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_reviews_collection = ProductReviewsCollection()
        return await product_reviews_collection.get_review_by_code(code=code,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/get_reviews_by_sku_code",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_reviews_by_sku_code(
    sku_code: str,
    page: int,
    limit: int,
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_reviews_collection = ProductReviewsCollection()
        return await product_reviews_collection.get_reviews_by_sku_code(sku_code=sku_code,page_number=page,limit=limit,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/upsert_reviews",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def upsert_blogs(
    product_reviews: List[ProductReviewCreateBaseModel],
    db: Session = Depends(auroradb.get_db)
):
    try:
        product_reviews_collection = ProductReviewsCollection()
        return await product_reviews_collection.upsert_multiple_reviews(product_reviews=product_reviews,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")