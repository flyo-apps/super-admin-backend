from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

    

class QuickFilterCreateModel(BaseModel):
    code: str
    screen_filter: dict
    data: List[dict]
    created_at: Optional[datetime] = datetime.now()
    is_updated: Optional[bool] = False
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    deleted_at: Optional[datetime] = None


class QuickFilterUpdateModel(BaseModel):
    data: List[dict]
    is_updated: bool = True
    updated_at: datetime = datetime.now()
