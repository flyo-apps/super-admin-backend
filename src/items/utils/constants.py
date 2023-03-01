
BRANDS_COL_RETURN = [
    "code", "brand_name", "sort_priority", "logo_image", "banner_image", "description", "description_images", "items_list", "search_tags"
]

BRANDS_COLLECTION_COL_RETURN = [
    "code", "brand_collection_name", "sort_priority", "brand_name", "collection_logo", "collection_banner", "description", "description_images", 
    "items_list", "search_tags"
]

PRODUCT_ITEMS_COL_RETURN = [
    'code', 'sku_code', 'media', 'discount', 'mrp', 'list_price', "brand", "product_name", "vendor_code", "product_tag", "fine_fashion_tag",
    "viewing_or_bought", "size", "category1", "product_type1", "pickup_city", "pick_pack_time"
]

CATEGORY_COL_RETURN = [
    "code", "category_name", "sort_priority", "category_logo", "category_banner", "description", "description_images", "items_list"
]

HOMEPAGE_COLLECTION_COL_RETURN = [
    "code", "homepage_collection_name", "images", "logo_images", "tags", "collection_discount", "collection_info", "redirect_to", 
    "redirect_type", "redirect_name", "filters", "products"
]

PRODUCT_COLLECTION_RETURN = [
    "collection_code", "collection_name", "sort_priority", "sku_code"
]

HOMEPAGE_COL_RETURN = [
    "code", "homepage_name", "component_title", "component_type", "component_elements_type", "component_elements", "component_rank", "component_secondary_title", 
    "widget_redirect_to", "component_category_link", "component_background_color", "ui_specs", "show_title", "max_visible_element", "h1_tag", "description_tag", "title_tag"
]

VALID_COMPONENT_TYPES = ["FWBanner", "FWImageCarousel", "FWITRCarousel", "FWITLCarousel", "BrandCard1", "BrandCard2", "CollectionCard1", "CollectionCard2", 
    "Product", "UsecaseList6", "ITOverlayCircle", "ITOverlaySquare", "ITOverlayCircle6", "CircleList", "FeaturedList4", "FilterChipList", "FilterImageList", 
    "ChipListSingle", "ChipListMulti", "VerticalList" 
]

VALID_COMPONENT_ELEMENTS_TYPE = [
    "Product", "Brand", "Category", "HomepageCollection", "BrandCollection", "Refer", "Filter", "ProductCollection", "Homepage"
]

VALID_ADD_TO_LIST = [
    "Brand", "BrandCollection", "Category", "Usecase", "Homepage"
]

VALID_HOMEPAGE_COMPONENT_NAMES_FOR_PAGES = [
   "Homepage_Brand", "Homepage_BrandCollection", "Homepage_Category", "Homepage_Usecase", "Homepage_Homepage"
]

PRODUCT_LIMIT = 30