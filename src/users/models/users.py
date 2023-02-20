from datetime import datetime
from typing import List, Optional, TypeVar
from db.mongo.mongo_model import OID, MongoModel
from master.models.master import BaseFullNameModel
from pydantic import BaseModel, Field, EmailStr


class UserProof(BaseModel):
    name: Optional[str] = None
    is_uploaded: Optional[bool] = False


class UserModel(BaseModel):
    referral_code_used: Optional[str] = None
    username: str
    full_name: Optional[BaseFullNameModel] = None
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None
    country: Optional[str] = None
    profile_image: Optional[str] = None
    guest_id: Optional[str] = None
    device_id: Optional[List[str]] = None
    fcm_token: Optional[List[str]] = None
    preferred_category: Optional[List[str]] = None
    gender: Optional[str] = None
    register_type: Optional[str] = None

class UserInModel(UserModel):
    referral_code: Optional[str] = None
    hashed_password: str
    whats_app_optin: Optional[bool]
    is_disabled: Optional[bool] = False
    is_deleted: Optional[bool] = False
    is_admin: Optional[bool] = False
    is_support: Optional[bool] = False
    is_guest: Optional[bool] = False
    created_on: Optional[datetime] = None
    disabled_on: Optional[datetime] = None
    deleted_on: Optional[datetime] = None

UD = TypeVar("UD", bound=UserInModel)


class UserOutModel(UserInModel, MongoModel):
    id: OID = Field()


class UserUpdateModel(MongoModel):
    full_name: Optional[BaseFullNameModel]
    mobile_number: Optional[str]
    email: Optional[EmailStr] = None
    preferred_category: Optional[List[str]] = None
    gender: Optional[str] = None


class UserUpdateCls(UserUpdateModel):
    username: Optional[str]
    is_updated: Optional[bool] = True
    is_disabled: Optional[bool] = False
    is_deleted: Optional[bool] = False
    updated_on: Optional[datetime] = None
    disabled_on: Optional[datetime] = None
    deleted_on: Optional[datetime] = None


class UserUpdateOutModel(UserUpdateCls):
    id: OID = Field()
