from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BlogCreateBaseModel(BaseModel):
    code: str
    blog_code: str
    blog_name: str
    blog_rank: Optional[int]
    blog_summary_image: str
    blog_type: str
    text: Optional[str] = None
    image: Optional[str] = None
    element_type: str
    element_code: Optional[str] = None
    filter: Optional[dict] = None
    width_percentage: float
    dimension: Optional[str] = None
    rank: Optional[int]


class BlogCreateModel(BlogCreateBaseModel):
    created_at: Optional[datetime] = datetime.now()
    is_updated: Optional[bool] = False
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    deleted_at: Optional[datetime] = None


class BlogUpdateBaseModel(BaseModel):
    code: str
    blog_code: str
    blog_name: str
    blog_rank: int
    blog_summary_image: Optional[str]
    blog_type: str
    text: Optional[str] = None
    image: Optional[str] = None
    element_type: str
    element_code: Optional[str] = None
    filter: Optional[dict] = None
    width_percentage: float
    dimension: Optional[str] = None
    rank: Optional[int]


class BlogUpdateModel(BlogUpdateBaseModel):
    is_updated: bool = True
    updated_at: datetime = datetime.now()


class BlogDeleteModel(BaseModel):
    code: str
    is_deleted: bool = True
    deleted_at: datetime = datetime.now()

class NewBlogCreateBaseModel(BaseModel):
    code: str
    screen_filter: Optional[dict]
    content: str
    content_summary: Optional[str]
    rank: Optional[int]

class NewBlogCreateModel(NewBlogCreateBaseModel):
    created_at: Optional[datetime] = datetime.now()
    is_updated: Optional[bool] = False
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    deleted_at: Optional[datetime] = None

class NewBlogUpdateBaseModel(BaseModel):
    code: str
    screen_filter: Optional[dict]
    content: Optional[str]
    content_summary: Optional[str]
    rank: Optional[int]

class NewBlogUpdateModel(NewBlogUpdateBaseModel):
    is_updated: bool = True
    updated_at: datetime = datetime.now()