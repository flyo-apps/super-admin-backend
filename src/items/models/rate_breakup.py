from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class RateBreakupCreateBaseModel(BaseModel):
    code: str
    brand: str
    metal: str
    rate: float
    weight_type: Optional[str] = None

class RateBreakupCreateModel(RateBreakupCreateBaseModel):
    created_at :  datetime = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class RateBreakupUpdateBaseModel(BaseModel):
    code: str
    brand: Optional[str] = None
    metal: Optional[str] = None
    rate: Optional[float] = None
    weight_type: Optional[str] = None

class RateBreakupUpdateModel(RateBreakupUpdateBaseModel):
    is_updated : bool = False
    updated_at : datetime = datetime.now()

class RateBreakupDeleteModel(BaseModel):
    code : str
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()