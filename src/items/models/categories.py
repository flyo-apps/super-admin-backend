from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class CategoryCreateBaseModel(BaseModel):
    code: str
    category_name: str
    sort_priority: Optional[int] = None
    category_logo: Optional[str] = None
    category_banner: Optional[str] = None
    description: Optional[str] = None
    description_images: Optional[List[str]] = []
    items_list: Optional[List[dict]] = []
    search_tags: Optional[List[str]] = []

class CategoryCreateModel(CategoryCreateBaseModel):
    created_at :  datetime = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None


class CategoryUpdateBaseModel(BaseModel):
    code: str
    category_name:Optional[str] = None
    sort_priority: Optional[int] = None
    category_logo: Optional[str] = None
    category_banner: Optional[str] = None
    description: Optional[str] = None
    description_images: Optional[List[str]] = []
    items_list: Optional[List[dict]] = []
    search_tags: Optional[List[str]] = []

class CategoryUpdateModel(CategoryUpdateBaseModel):
    is_updated : bool = False
    updated_at : Optional[datetime] = datetime.now()

class CategoryDeleteModel(BaseModel):
    code : str
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()


