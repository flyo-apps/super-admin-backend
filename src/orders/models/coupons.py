from datetime import datetime
from typing import List, Optional
from db.mongo.mongo_model import OID, MongoModel
from pydantic import BaseModel, Field

class CouponCreateBaseModel(MongoModel):
    title: str = ""
    instructions: str = ""
    tnc: str = ""
    coupon_type: str = ""
    coupon_code: str
    coupon_name: str = ""
    instructions: Optional[str] = None
    tnc: Optional[str] = None
    coupon_type: Optional[str] = None
    specs_entity: str = "Cart"
    discounted_entity: str = "Cart"
    discount_percent: float = 0.0
    discount_cap: float = 0.0
    min_aov: float = 0.0
    location_specs: Optional[dict] = None
    times_valid: Optional[float] = None
    username: Optional[str] = None
    user_specs: Optional[dict] = None
    past_orders_specs: Optional[dict] = None
    date_specs: Optional[dict] = None
    other_specs: Optional[dict] = None
    product_groups: Optional[list] = None
    is_hidden: bool = True
    is_visible_if_invalid: bool = False

class CouponCreateModel(CouponCreateBaseModel):
    is_deleted: Optional[bool] = False
    is_updated: Optional[bool] = False
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    deleted_on: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CouponUpdateBaseModel(BaseModel):
    title: Optional[str] = None
    instructions: Optional[str] = None
    tnc: Optional[str] = None
    coupon_type: Optional[str] = None
    coupon_code: Optional[str]
    coupon_name: Optional[str] = None
    instructions: Optional[str] = None
    tnc: Optional[str] = None
    coupon_type: Optional[str] = None
    specs_entity: Optional[str] = None
    discounted_entity: Optional[str] = None
    discount_percent: Optional[float] = None
    discount_cap: Optional[float] = None
    min_aov: Optional[float] = None
    location_specs: Optional[dict] = None
    times_valid: Optional[float] = None
    username: Optional[str] = None
    user_specs: Optional[dict] = None
    past_orders_specs: Optional[dict] = None
    date_specs: Optional[dict] = None
    other_specs: Optional[dict] = None
    product_groups: Optional[list] = None
    is_hidden: Optional[bool] = None
    is_visible_if_invalid: Optional[bool] = None

class CouponUpdateModel(CouponUpdateBaseModel):
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = datetime.now()

class CouponsModelOut(CouponCreateBaseModel):
    id: OID = Field()

class CouponsModelOutList(MongoModel):
    coupons_list: List[CouponsModelOut]
