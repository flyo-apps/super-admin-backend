from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class MultiStoryCreateBaseModel(BaseModel):
    code: str
    story_name: str
    story_logo: str
    description: Optional[str] = None
    stories: List[dict]

class MultiStoryCreateModel(MultiStoryCreateBaseModel):
    created_at :  datetime = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class MultiStoryUpdateBaseModel(BaseModel):
    code: str
    story_name: str
    story_logo: str
    description: Optional[str] = None
    stories: Optional[List[dict]] = None

class MultiStoryUpdateModel(MultiStoryUpdateBaseModel):
    is_updated : bool = False
    updated_at : datetime = datetime.now()

class MultiStoryDeleteModel(BaseModel):
    code : str
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()