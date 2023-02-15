from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class BrandsCollectionCreateBaseModel(BaseModel):
    code: str
    brand_collection_name: str
    sort_priority: Optional[int] = None
    brand_name : Optional[str] = None
    collection_logo: Optional[str] = None
    collection_banner: Optional[str] = None
    description: Optional[str] = None
    description_images: Optional[List[str]] = None
    items_list: Optional[List[dict]] = None
    search_tags: Optional[List[str]] = None

class BrandsCollectionCreateModel(BrandsCollectionCreateBaseModel):
    created_at : Optional[datetime] = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class BrandsCollectionUpdateBaseModel(BaseModel):
    code: str
    brand_collection_name: Optional[str] = None
    sort_priority: Optional[int] = None
    brand_name : Optional[str] = None
    collection_logo: Optional[str] = None
    collection_banner: Optional[str] = None
    description: Optional[str] = None
    description_images: Optional[List[str]] = []
    items_list: Optional[List[dict]] = []
    search_tags: Optional[List[str]] = []

class BrandsCollectionUpdateModel(BrandsCollectionUpdateBaseModel):
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = datetime.now()

class BrandsCollectionDeleteModel(BaseModel):
    code : str
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()