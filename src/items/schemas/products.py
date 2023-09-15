from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, Integer, String, Float, ARRAY, JSON, DATETIME


class ProductsSchema(Base):
    __tablename__ = "products"

    code = Column(String, primary_key=True, index=True)
    sku_code = Column(String, index=True)
    product_code = Column(String)
    product_name = Column(String)
    brand = Column(String)
    brand_code = Column(String)
    upc = Column(String)
    hsn = Column(String)
    category1 = Column(String)
    category2 = Column(String)
    category3 = Column(String)
    usecase1 = Column(String)
    usecase2 = Column(String)
    usecase3 = Column(String)
    usecase4 = Column(String)
    usecase5 = Column(String)
    product_type1 = Column(String)
    product_type2 = Column(String)
    product_type3 = Column(String)
    style_code = Column(String)
    collection = Column(String)
    vendor = Column(String)
    vendor_sku_code = Column(String)
    gender = Column(String)
    size = Column(String)
    size_unit = Column(String)
    metal1 = Column(String)
    metal2 = Column(String)
    metal3 = Column(String)
    material1 = Column(String)
    material2 = Column(String)
    material3 = Column(String)
    stone1 = Column(String)
    stone2 = Column(String)
    stone3 = Column(String)
    colour1 = Column(String)
    colour2 = Column(String)
    colour3 = Column(String)
    metal_colour1 = Column(String)
    metal_colour2 = Column(String)
    metal_colour3 = Column(String)
    style_of_jewellery = Column(String)
    plating = Column(String)
    warranty = Column(String)
    shipping_time = Column(String)
    purity = Column(String)
    designer = Column(String)
    gifting = Column(Boolean)
    virtual_try_on = Column(Boolean)
    description = Column(String)
    description_images = Column(ARRAY(String))
    guide_images = Column(ARRAY(String))
    care_instruction = Column(String)
    disclaimer = Column(String)
    year = Column(Integer)
    season = Column(String)
    certificate_type = Column(String)
    search_tags = Column(ARRAY(String))
    weight = Column(Float)
    weight_unit = Column(String)
    seller_panel = Column(String)
    mrp = Column(Float)
    msp = Column(Float)
    gst_percent = Column(Integer)
    list_price = Column(Float)
    media = Column(ARRAY(JSON))
    items_list = Column(ARRAY(JSON))
    returnable = Column(Boolean)
    returnable_policy = Column(String)
    replaceable = Column(String)
    replaceable_policy = Column(String)
    only_prepaid = Column(Boolean)
    seo_title = Column(String)
    seo_description = Column(String)
    seo_canonical_url = Column(String)
    seo_tags = Column(String)
    seo_keywords = Column(ARRAY(String))
    is_bestseller = Column(Boolean)
    google_product_category = Column(String)
    age_group = Column(String)
    mpn = Column(String)
    adwords_grouping = Column(String)
    adwords_label = Column(String)
    condition = Column(String)
    custom_product = Column(String)
    custom_label = Column(ARRAY(String))
    live = Column(Boolean)
    country_of_origin = Column(String)
    discount = Column(Float)
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)
    sort_priority1 = Column(Integer)
    sort_priority2 = Column(Integer)
    sort_priority3 = Column(Integer)
    sort_priority4 = Column(Integer)
    sort_priority5 = Column(Integer)
    products_list = Column(ARRAY(JSON))
    manufacturer_name = Column(String)
    manufacturer_address = Column(String)
    is_customizable = Column(Boolean)
    production_strategy = Column(String)
    vendor_code = Column(String)
    product_tag = Column(String)
    fine_fashion_tag = Column(String)
    pdp_strip_images = Column(ARRAY(JSON))
    viewing_or_bought = Column(String)
    manufacturer_pincode = Column(String)
    pickup_city= Column(String)
    production_strategy = Column(String)
    finish_and_design = Column(String)
    brand_description_images = Column(ARRAY(String))
    brand_offer_strip = Column(ARRAY(JSON))
    style_note = Column(String)
    design_type = Column(String)
    express_shipping = Column(Boolean)
    collection2 = Column(String)
    collection3 = Column(String)
    collection4 = Column(String)
    pick_pack_time = Column(Integer)
    title_tag = Column(String)
    description_tag = Column(String)
    h1_tag = Column(String)
    complete_the_look_skus = Column(ARRAY(String))
    certificate_image = Column(String)
    product_details = Column(JSON)
    price_breakup = Column(ARRAY(JSON))
    people_also_explored = Column(ARRAY(JSON))
