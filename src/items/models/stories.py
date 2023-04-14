from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class StoryCreateBaseModel(BaseModel):
    code: str
    story_name: str
    story_logo: str
    story_image: Optional[str] = None
    description: Optional[str] = None
    redirection_type: str
    redirection_text: str
    redirection_value: str
    filters: Optional[dict] = None

class StoryCreateModel(StoryCreateBaseModel):
    created_at :  datetime = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class StoryUpdateBaseModel(BaseModel):
    code: str
    story_name: str
    story_logo: str
    story_image: Optional[str] = None
    description: Optional[str] = None
    redirection_type: str
    redirection_text: str
    redirection_value: str
    filters: Optional[dict] = None

class StoryUpdateModel(StoryUpdateBaseModel):
    is_updated : bool = False
    updated_at : datetime = datetime.now()

class StoryDeleteModel(BaseModel):
    code : str
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()