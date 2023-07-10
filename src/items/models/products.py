from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class ProductQNAModel(BaseModel):
    code: str
    question: str
    answer: str
    created_at: Optional[str]

class ProductCreateBaseModel(BaseModel):
    code : str
    sku_code : str
    product_name : str
    brand : str
    upc : Optional[str] = ""
    hsn : str
    mrp : float
    msp : float
    gst_percent: int
    list_price : float
    vendor : str
    gender : str
    vendor_code: str
    size : Optional[str] = ""
    category1 : str
    category2 : Optional[str] = None
    category3 : Optional[str] = None
    usecase1 : Optional[str] = None
    usecase2 : Optional[str] = None
    usecase3 : Optional[str] = None
    usecase4 : Optional[str] = None
    usecase5 : Optional[str] = None
    size_unit : Optional[str] = None
    product_type1 : Optional[str] = None
    product_type2 : Optional[str] = None
    product_type3 : Optional[str] = None
    vendor_sku_code : Optional[str] = None
    style_code : Optional[str] = None
    collection : Optional[str] = None
    metal1 : Optional[str] = None
    metal2 : Optional[str] = None
    metal3 : Optional[str] = None
    material1 : Optional[str] = None
    material2 : Optional[str] = None
    material3 : Optional[str] = None
    stone1 : Optional[str] = None
    stone2 : Optional[str] = None
    stone3 : Optional[str] = None
    colour1 : Optional[str] = None
    colour2 : Optional[str] = None
    colour3 : Optional[str] = None
    metal_colour1 : Optional[str] = None
    metal_colour2 : Optional[str] = None
    metal_colour3 : Optional[str] = None
    style_of_jewellery : Optional[str] = None
    product_tag: Optional[str] = None
    fine_fashion_tag: Optional[str] = None
    pdp_strip_images: Optional[List[dict]] = None
    viewing_or_bought: Optional[str] = None
    plating : Optional[str] = None
    warranty : Optional[str] = None
    shipping_time : Optional[str] = None
    purity : Optional[str] = None
    designer : Optional[str] = None
    gifting : Optional[bool] = False
    virtual_try_on : Optional[bool] = False
    description : Optional[str] = None
    description_images : Optional[List[str]] = []
    care_instruction : Optional[str] = None
    disclaimer : Optional[str] = None
    year : Optional[int] = None
    season : Optional[str] = None
    certificate_type : Optional[str] = None
    search_tags : Optional[List[str]] = []
    weight : Optional[float] = None
    weight_unit : Optional[str] = None
    seller_panel : Optional[str] = None
    media : List[dict]
    items_list: Optional[List[dict]] = None
    returnable : Optional[bool] = None
    returnable_policy : Optional[str] = None
    replaceable : Optional[bool] = None
    replaceable_policy : Optional[str] = None
    only_prepaid : Optional[bool] = None
    seo_title : Optional[str] = None
    seo_description : Optional[str] = None
    seo_canonical_url : Optional[str] = None
    seo_tags : Optional[str] = None
    seo_keywords: Optional[List[str]] = None
    is_bestseller : Optional[bool] = None
    google_product_category : Optional[str] = None
    age_group : Optional[str] = None
    mpn : Optional[str] = None
    adwords_grouping : Optional[str] = None
    adwords_label : Optional[str] = None
    condition : Optional[str] = None
    custom_product : Optional[str] = None
    custom_label : Optional[List[str]] 
    live : Optional[bool] = True
    country_of_origin : Optional[str] = None
    discount : Optional[float] = 0
    sort_priority1: Optional[int] = 0
    sort_priority2: Optional[int] = 0
    sort_priority3: Optional[int] = 0
    sort_priority4: Optional[int] = 0
    sort_priority5: Optional[int] = 0
    products_list: Optional[List[dict]] = []
    manufacturer_name: Optional[str] = None
    manufacturer_address: Optional[str] = None
    manufacturer_pincode: Optional[str]
    production_strategy: Optional[str] = None
    is_customizable: Optional[bool] = False
    pickup_city: Optional[str] = None
    finish_and_design: Optional[str] = None
    brand_description_images: Optional[List[str]] = None
    brand_offer_strip: Optional[List[dict]] = None
    style_note: Optional[str] = None
    design_type: Optional[str] = None
    express_shipping: Optional[bool] = None
    collection2: Optional[str] = None
    collection3: Optional[str] = None
    collection4: Optional[str] = None
    pick_pack_time: Optional[int] = None
    title_tag: Optional[str] = None
    description_tag: Optional[str] = None
    h1_tag: Optional[str] = None
    qnas: Optional[List[ProductQNAModel]] = None
    complete_the_look_skus: Optional[List[str]] = None

class ProductCreateModel(ProductCreateBaseModel):
    created_at : Optional[datetime] = datetime.now()
    is_updated : Optional[bool] = False
    updated_at : Optional[datetime] = None
    is_deleted : Optional[bool] = False
    deleted_at : Optional[datetime] = None

class ProductUpdateBaseModel(BaseModel):
    code : str
    sku_code : str
    product_name : Optional[str] 
    brand : Optional[str] 
    upc : Optional[str] 
    hsn : Optional[str] 
    category1 : Optional[str] 
    category2 : Optional[str] 
    category3 : Optional[str] 
    usecase1 : Optional[str] 
    usecase2 : Optional[str] 
    usecase3 : Optional[str]
    usecase4 : Optional[str]
    usecase5 : Optional[str]
    product_type1 : Optional[str]
    product_type2 : Optional[str]
    product_type3 : Optional[str]
    style_code : Optional[str]
    collection : Optional[str]
    vendor : Optional[str]
    vendor_sku_code : Optional[str]
    vendor_code: Optional[str]
    gender : Optional[str]
    size : Optional[str]
    size_unit : Optional[str]
    metal1 : Optional[str]
    metal2 : Optional[str]
    metal3 : Optional[str]
    material1 : Optional[str]
    material2 : Optional[str]
    material3 : Optional[str]
    stone1 : Optional[str]
    stone2 : Optional[str]
    stone3 : Optional[str]
    colour1 : Optional[str]
    colour2 : Optional[str]
    colour3 : Optional[str]
    metal_colour1 : Optional[str]
    metal_colour2 : Optional[str]
    metal_colour3 : Optional[str]
    style_of_jewellery : Optional[str]
    plating : Optional[str]
    warranty : Optional[str]
    purity : Optional[str]
    designer : Optional[str]
    disclaimer : Optional[str]
    year : Optional[int]
    season : Optional[str]
    certificate_type : Optional[str]
    weight : Optional[float]
    weight_unit : Optional[str]
    seller_panel : Optional[str]
    mrp : Optional[float]
    gst_percent: Optional[float]
    msp : Optional[float]
    list_price : Optional[float]
    age_group : Optional[str]
    mpn : Optional[str]
    country_of_origin : Optional[str]
    discount : Optional[float]
    sort_priority1: Optional[int] = None
    sort_priority2: Optional[int] = None
    sort_priority3: Optional[int] = None
    sort_priority4: Optional[int] = None
    sort_priority5: Optional[int] = None
    products_list: Optional[List[dict]]
    is_customizable: Optional[bool] 
    pickup_city: Optional[str] = None
    production_strategy: Optional[str] = None
    finish_and_design: Optional[str] = None
    brand_description_images: Optional[List[str]] = None
    brand_offer_strip: Optional[List[dict]] = None
    style_note: Optional[str] = None
    design_type: Optional[str] = None
    express_shipping: Optional[bool] = None
    collection2: Optional[str] = None
    collection3: Optional[str] = None
    collection4: Optional[str] = None
    pick_pack_time: Optional[int] = None
    qnas: Optional[List[ProductQNAModel]] = None
    complete_the_look_skus: Optional[List[str]] = None


class ProductUpdateModel(ProductUpdateBaseModel):
    is_updated : Optional[bool] = True
    updated_at : Optional[datetime] = datetime.now()
    
class ProductUpdateStateBaseModel(BaseModel):
    code : str
    sku_code : str
    live : Optional[bool]
    returnable : Optional[bool]
    returnable_policy : Optional[str]
    replaceable : Optional[bool]
    replaceable_policy : Optional[str]
    search_tags : Optional[List[str]]
    product_tag: Optional[str] = None
    fine_fashion_tag: Optional[str] = None
    viewing_or_bought: Optional[str] = None
    virtual_try_on : Optional[bool]
    is_bestseller : Optional[bool]
    condition : Optional[str]
    gifting : Optional[bool]
    shipping_time : Optional[str]
    only_prepaid : Optional[bool]
    manufacturer_name: Optional[str]
    manufacturer_address: Optional[str] 
    manufacturer_pincode: Optional[str]

class ProductUpdateStateModel(ProductUpdateStateBaseModel):
    is_updated : Optional[bool] = True
    updated_at : Optional[datetime] = datetime.now()


class ProductUpdateDescriptionBaseModel(BaseModel):
    code : str
    sku_code : str
    description : Optional[str]
    description_images : Optional[List[str]]
    care_instruction : Optional[str]
    media : Optional[List[dict]]
    pdp_strip_images: Optional[List[dict]] = None
    items_list : Optional[List[dict]]
    title_tag: Optional[str] = None
    description_tag: Optional[str] = None
    h1_tag: Optional[str] = None

class ProductUpdateDescriptionModel(ProductUpdateDescriptionBaseModel):
    is_updated : Optional[bool] = True
    updated_at : Optional[datetime] = datetime.now()


class ProductUpdateSeoBaseModel(BaseModel):
    code : str
    sku_code : str 
    seo_title : Optional[str]
    seo_description : Optional[str]
    seo_canonical_url : Optional[str]
    seo_tags : Optional[str]
    seo_keywords : Optional[List[str]] 
    google_product_category : Optional[str]
    custom_product : Optional[str]
    custom_label : Optional[List[str]] 
    adwords_grouping : Optional[str]
    adwords_label : Optional[str]

class ProductUpdateSeoModel(ProductUpdateSeoBaseModel):
    is_updated : Optional[bool] = True
    updated_at : Optional[datetime] = datetime.now()

class ProductDeleteModel(BaseModel):
    code : str
    live: bool = False
    is_deleted : bool = True
    deleted_at : datetime = datetime.now()




