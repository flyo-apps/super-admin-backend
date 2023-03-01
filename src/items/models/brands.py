from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class BrandCreateBaseModel(BaseModel):
    code: str
    brand_name: str
    sort_priority: Optional[int] = None
    logo_image: Optional[str] = None
    banner_image: Optional[str] = None
    description: Optional[str] = None
    description_images: Optional[List[str]] = []
    items_list: Optional[List[dict]] = []
    search_tags: Optional[List[str]] = []
    has_store: Optional[bool] = False

class BrandCreateModel(BrandCreateBaseModel):
    created_at : Optional[datetime] = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class BrandUpdateBaseModel(BaseModel):
    code: str
    brand_name: Optional[str]
    sort_priority: Optional[int] = None
    logo_image: Optional[str] = None
    banner_image: Optional[str] = None
    description: Optional[str] = None
    description_images: Optional[List[str]] = []
    items_list: Optional[List[dict]] = []
    search_tags: Optional[List[str]] = []
    has_store: Optional[bool] = False

class BrandUpdateModel(BrandUpdateBaseModel):
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = datetime.now()

class BrandDeleteModel(BaseModel):
    code : str
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()