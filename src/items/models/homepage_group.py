from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class CreateHomePageCollectionBaseModel(BaseModel):
    code: str
    homepage_collection_name: str
    images: Optional[List[str]] = []
    logo_images: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    collection_discount: Optional[float] = None
    collection_info: Optional[str] = None
    redirect_to: Optional[str] = None
    redirect_type: Optional[str] = None
    redirect_name: Optional[str] = None

class CreateHomePageCollectionModel(CreateHomePageCollectionBaseModel):
    filters: Optional[List[str]] = []
    products: Optional[List[str]] = []
    created_at: Optional[datetime] = datetime.now()
    is_updated: Optional[bool] = False
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    deleted_at: Optional[datetime] = None

class UpdateHomePageCollectionBaseModel(BaseModel):
    code: str
    homepage_collection_name: str
    images: Optional[List[str]] = []
    logo_images: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    collection_discount: Optional[float] = None
    collection_info: Optional[str] = None
    redirect_type: Optional[str] = None
    redirect_name: Optional[str] = None

class UpdateHomePageCollectionModel(UpdateHomePageCollectionBaseModel):
    redirect_to: Optional[str] = None
    is_updated: Optional[bool] = True
    updated_at: Optional[datetime] = datetime.now()



