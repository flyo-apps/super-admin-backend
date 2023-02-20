from datetime import datetime, date
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class ProductReviewCreateBaseModel(BaseModel):
    code: str
    sku_code: str
    title: Optional[str]
    review: str
    rating: float
    customer_name: str
    created_at: Optional[date]

class ProductReviewCreateModel(ProductReviewCreateBaseModel):
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class ProductReviewUpdateBaseModel(BaseModel):
    code: str
    sku_code: str
    title: Optional[str]
    review: str
    rating: float
    customer_name: str
    created_at: Optional[date]


class ProductReviewUpdateModel(ProductReviewUpdateBaseModel):
    is_updated : bool = True
    updated_at : datetime = datetime.now()

class ProductReviewDeleteModel(BaseModel):
    code: str
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()            