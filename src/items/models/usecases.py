from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UsecaseCreateBaseModel(BaseModel):
    code: str
    usecase_name: str
    sort_priority: Optional[int] = None
    usecase_logo: Optional[str] = None
    usecase_banner: Optional[str] = None
    description: Optional[str] = None
    description_images: Optional[List[str]] = []
    items_list: Optional[List[dict]] = []
    search_tags: Optional[List[str]] = []

class UsecaseCreateModel(UsecaseCreateBaseModel):
    created_at : Optional[datetime] = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class UsecaseUpdateBaseModel(BaseModel):
    code: str
    usecase_name: Optional[str] = None
    sort_priority: Optional[int] = None
    usecase_logo: Optional[str] = None
    usecase_banner: Optional[str] = None
    description: Optional[str] = None
    description_images: Optional[List[str]] = []
    items_list: Optional[List[dict]] = []
    search_tags: Optional[List[str]] = []

class UsecaseUpdateModel(UsecaseUpdateBaseModel):
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = datetime.now()

class UsecaseDeleteModel(BaseModel):
    code : str
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()