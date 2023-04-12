from datetime import datetime
from typing import List, Optional

from db.mongo.mongo_model import OID, MongoModel
from pydantic import BaseModel, Field

class BaseCategoriesModel(MongoModel):
    title: str = ""
    images: Optional[List[str]] = []
    logo_images: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    sort_priority_category: Optional[float] = 0
    category_discount: Optional[int] = 0

class CreateCategoryFullModel(BaseCategoriesModel):
    is_subcategory: Optional[bool] = False
    parent_category: Optional[str] = None
    product_types: Optional[List[str]] = []
    filters: Optional[List[str]] = []
    subcategories: Optional[List[OID]] = []
    brands: Optional[List[OID]] = []
    top_brands: Optional[List[OID]] = []
    new_brands: Optional[List[OID]] = []
    top_products: Optional[List[OID]] = []
    new_products: Optional[List[OID]] = []
    trending_products: Optional[List[OID]] = []
    discounted_products: Optional[List[OID]] = []

class CreateCategoriesModelIn(CreateCategoryFullModel):
    is_deleted: Optional[bool] = False
    is_disabled: Optional[bool] = False
    is_updated: Optional[bool] = False
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    deleted_on: Optional[datetime] = None
    disabled_on: Optional[datetime] = None

class CreateCategoriesModelOut(BaseCategoriesModel):
    id: OID = Field()

class CreateCategoryFullModelOut(CreateCategoryFullModel):
    id: OID = Field()

class CreateCategoriesModelOutList(MongoModel):
    categories_list: List[CreateCategoriesModelOut]

class CreateCategoryFullModelOutList(MongoModel):
    categories_list: List[CreateCategoryFullModelOut]


class CategoryCreateBaseModel(BaseModel):
    code: str
    category_name: str
    sort_priority: Optional[int] = None
    category_logo: Optional[str] = None
    category_banner: Optional[str] = None
    description: Optional[str] = None
    description_images: Optional[List[str]] = []
    items_list: Optional[List[dict]] = []
    search_tags: Optional[List[str]] = []

class CategoryCreateModel(CategoryCreateBaseModel):
    created_at :  datetime = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None


class CategoryUpdateBaseModel(BaseModel):
    code: str
    category_name:Optional[str] = None
    sort_priority: Optional[int] = None
    category_logo: Optional[str] = None
    category_banner: Optional[str] = None
    description: Optional[str] = None
    description_images: Optional[List[str]] = []
    items_list: Optional[List[dict]] = []
    search_tags: Optional[List[str]] = []

class CategoryUpdateModel(CategoryUpdateBaseModel):
    is_updated : bool = False
    updated_at : Optional[datetime] = datetime.now()

class CategoryDeleteModel(BaseModel):
    code : str
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()