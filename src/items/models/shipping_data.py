from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class ShippingDataCreateBaseModel(BaseModel):
    code : constr(to_lower=True)
    seller_warehouse : constr(to_lower=True)
    drop_city : constr(to_lower=True)
    drop_pincode : str
    drop_state : Optional[constr(to_lower=True)]
    tat: int

class ShippingDataCreateModel(ShippingDataCreateBaseModel):
    created_at : Optional[datetime] = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class ShippingDataUpdateBaseModel(BaseModel):
    code : constr(to_lower=True)
    seller_warehouse : constr(to_lower=True)
    drop_city : constr(to_lower=True)
    drop_pincode : str
    drop_state : Optional[constr(to_lower=True)]
    tat: int

class ShippingDataUpdateModel(ShippingDataUpdateBaseModel):
    is_updated : Optional[bool] = True
    updated_at : Optional[datetime] = datetime.now()

class ShippingDataDeleteModel(BaseModel):
    code: constr(to_lower=True)
    is_deleted: bool = True
    deleted_at: datetime = datetime.now()