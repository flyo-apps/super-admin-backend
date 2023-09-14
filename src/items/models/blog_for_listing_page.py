from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BlogForListPageCreateBaseModel(BaseModel):
    code: str
    image: str
    rank: int
    screen_filter: dict 
    blog_code: str

class BlogForListPageCreateModel(BlogForListPageCreateBaseModel):
    created_at :  datetime = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class BlogForListPageUpdateBaseModel(BaseModel):
    code: str
    image: Optional[str] = None
    rank: Optional[int] = None
    screen_filter: Optional[dict] = None
    blog_code: Optional[str] = None


class BlogForListPageUpdateModel(BlogForListPageUpdateBaseModel):
    is_updated : bool = False
    updated_at : datetime = datetime.now()

class BlogForListPageDeleteModel(BaseModel):
    code : str
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()