from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ProductCollectionCreateBaseModel(BaseModel):
    code: str
    collection_name: str
    collection_details: Optional[str] = None
    search_tags: Optional[List] = None
    collection_images: Optional[List] = None

class ProductCollectionCreateModel(ProductCollectionCreateBaseModel):
    created_at : Optional[datetime] = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None

class ProductCollectionUpdateBaseModel(BaseModel):
    code: str
    collection_name: Optional[str] = None
    collection_details: Optional[str] = None
    search_tags: Optional[List] = None
    collection_images: Optional[List] = None

class ProductCollectionUpdateModel(ProductCollectionUpdateBaseModel):
    is_updated : bool = True
    updated_at : datetime = datetime.now()