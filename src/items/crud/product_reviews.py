from db.aurora.aurora_base import CRUDBase
from items.models.product_reviews import ProductReviewCreateBaseModel, ProductReviewCreateModel, ProductReviewDeleteModel, ProductReviewUpdateBaseModel, ProductReviewUpdateModel
from ..schemas.product_reviews import ProductReviewSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

class ProductReviewsCollection:
    def __init__(self):
        self.model = CRUDBase(ProductReviewSchema)

    async def add_review(
        self,
        review: ProductReviewCreateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{review.code}'"""
            existing_review = self.model.get_one(db=db, where_clause=where_clause)
            if existing_review is not None:
                return {"internal_response_code": 1, "message": f"""review with code {review.code} exists"""}

            review_create = ProductReviewCreateModel(**review.dict())
            created_review = self.model.create(db=db, obj_in=review_create)

            return {"internal_response_code": 0, "message": f"""created review with code {review.code}""" } if created_review else {"internal_response_code": 1, "message": f"""failed to create review with code {review.code}"""}
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_review(
        self,
        review: ProductReviewUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{review.code}' AND is_deleted=False"""
            existing_review = self.model.get_one(db=db, where_clause=where_clause)
            if existing_review is None:
                return {"internal_response_code": 1, "message": f"""review with code {review.code} not found"""}

            review_update = ProductReviewUpdateModel(**review.dict())
            review_update_dict = review_update.dict()
            updated_review = self.model.update(db=db, db_obj=existing_review,obj_in=review_update_dict)

            return {"internal_response_code": 0, "message": f"""updated review with code {review.code}""" } if updated_review else {"internal_response_code": 1, "message": f"""failed to update review with code {review.code}"""}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def delete_review(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{code}' AND is_deleted=False"""
            existing_review = self.model.get_one(db=db, where_clause=where_clause)
            if existing_review is None:
                return {"internal_response_code": 1, "message": f"""review with code {code} not found"""}

            review_delete = ProductReviewDeleteModel(code=code)
            review_delete_dict = review_delete.dict()
            deleted_review = self.model.update(db=db, db_obj=existing_review, obj_in=review_delete_dict)

            return {"internal_response_code": 0, "message": f"""deleted review with code {code}""" } if deleted_review else {"internal_response_code": 1, "message": f"""failed to delete review with code {code}"""}             
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_review_by_code(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{code}' AND is_deleted=False"""
            existing_review = self.model.get_one(db=db, where_clause=where_clause)

            return {"internal_response_code": 0, "data": existing_review} if existing_review else {"internal_response_code": 1, "message": f"""review with code {code} not found"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_reviews_by_sku_code(
        self,
        sku_code: str,
        page_number: int,
        limit: int,
        db: Session
    ) -> any:
        try:
            where_clause = f"""sku_code='{sku_code}' AND is_deleted=False"""
            skip=0
            if page_number >1 :
                skip = (page_number - 1)*limit
            reviews = self.model.get_all(db=db, where_clause=where_clause, skip=skip, limit=limit)

            return {"internal_response_code": 0, "data": reviews}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def upsert_multiple_reviews(
        self,
        product_reviews: List[ProductReviewCreateBaseModel],
        db: Session
    ) -> any:
        try:
            review_codes = ','.join(["'" + data.code + "'" for data in product_reviews])
            existing_codes = []
            where_clause = f"""code IN ({review_codes})"""
            existing_reviews = self.model.get_all(
                db=db, where_clause=where_clause, skip=0, limit=len(product_reviews))
            if existing_reviews:
                existing_codes = [data.code for data in existing_reviews]

            reviews_create = []
            reviews_update = []
            for review in product_reviews:
                if review.code not in existing_codes:
                    review_create = ProductReviewCreateModel(**review.dict())
                    reviews_create.append(review_create.dict())
                else:
                    review_update = ProductReviewUpdateModel(**review.dict())
                    reviews_update.append(review_update.dict())

            res = self.model.bulk_upsert(
                db=db, update_vals=reviews_update, insert_vals=reviews_create)
            return {"internal_response_code": 0, "message": f"""reviews created for {len(reviews_create)} codes and updated for {len(reviews_update)} codes"""} if res is None else {"internal_response_code": 1, "message": f"""upsert operation failed"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")
