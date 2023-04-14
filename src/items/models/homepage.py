from datetime import datetime
from typing import List, Optional
from db.mongo.mongo_model import OID, MongoModel
from pydantic import BaseModel, Field

class BaseHomePageComponentModel(MongoModel):
    component_title: str
    component_type: str
    component_elements_type: str
    component_elements: List
    component_rank: int
    show_title: Optional[bool] = False
    max_visible_element: Optional[int] = 10
    component_secondary_title: Optional[str] = None
    widget_redirect_to: Optional[str] = None
    component_category_link: Optional[OID] = None
    component_background_color: Optional[str] = None

class HomePageModel(BaseHomePageComponentModel):
    title: str

class HomePageModelIn(HomePageModel):
    is_deleted: Optional[bool] = False
    is_disabled: Optional[bool] = False
    is_updated: Optional[bool] = False
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    deleted_on: Optional[datetime] = None
    disabled_on: Optional[datetime] = None

class HomePageModelOut(HomePageModel):
    id: OID = Field()

class HomePageModelOutList(MongoModel):
    homepage_details: List[HomePageModelOut]


class HomePageCreateBaseModel(BaseModel):
    code: str
    homepage_name: Optional[str] = "Primary"
    component_title: str
    title_tag : str
    description_tag : str
    h1_tag : str
    component_type: str
    component_elements_type: str
    type: Optional[str] = None
    show_title: Optional[bool] = False
    max_visible_element: Optional[int] = 10
    component_rank: Optional[int] = None
    component_secondary_title: Optional[str] = None
    widget_redirect_to: Optional[str] = None
    component_category_link: Optional[str] = None
    component_background_color: Optional[str] = None
    ui_specs: Optional[dict] = None

class HomePageCreateModel(HomePageCreateBaseModel):
    component_elements: Optional[List[dict]] = []
    created_at : Optional[datetime] = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class HomePageUpdateBaseModel(BaseModel):
    code: str
    homepage_name: str
    component_title: str
    title_tag: str
    description_tag: str
    h1_tag: str
    component_type: Optional[str]
    component_elements_type: Optional[str]
    show_title: Optional[bool] = False
    max_visible_element: Optional[int] = 10
    type: Optional[str] 
    component_rank: Optional[int] 
    component_secondary_title: Optional[str]
    widget_redirect_to: Optional[str]
    component_category_link: Optional[str]
    component_background_color: Optional[str]
    ui_specs: Optional[dict]

class HomePageUpdateModel(HomePageUpdateBaseModel):
    is_updated : bool = True
    updated_at : datetime = datetime.now()

class HomePageElementsBaseUpdateModel(BaseModel):
    component_elements: List[dict] = []

class HomePageElementsUpdateModel(HomePageElementsBaseUpdateModel):
    is_updated : bool = True
    updated_at : datetime = datetime.now()


class HomePageFilterDetails(BaseModel):
    filters: Optional[dict] = None
    secondary_title: Optional[str] = None
    sorting_method: Optional[str] = None
    filter_type: Optional[str] = None

class HomePageDeleteModel(BaseModel):
    code: str
    is_deleted: bool = True
    deleted_at: datetime = datetime.now()