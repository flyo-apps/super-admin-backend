from ..schemas.homepage import HomepageSchema
from ..schemas.categories import CategoriesSchema
from ..schemas.brands_collection import BrandsCollectionSchema


BRANDS_COL_RETURN = [
    "code", "brand_name", "sort_priority", "logo_image", "banner_image", "description", "description_images", "items_list", "search_tags"
]

BRANDS_COLLECTION_COL_RETURN = [
    BrandsCollectionSchema.code, BrandsCollectionSchema.brand_collection_name, BrandsCollectionSchema.sort_priority, BrandsCollectionSchema.brand_name, BrandsCollectionSchema.collection_logo, BrandsCollectionSchema.collection_banner, BrandsCollectionSchema.description, BrandsCollectionSchema.description_images,
    BrandsCollectionSchema.items_list, BrandsCollectionSchema.search_tags
]

PRODUCT_ITEMS_COL_RETURN = [
    'code', 'sku_code', 'media', 'discount', 'mrp', 'list_price', "brand", "product_name", "vendor_code", "product_tag", "fine_fashion_tag",
    "viewing_or_bought", "size", "category1", "product_type1", "pickup_city", "pick_pack_time"
]

CATEGORY_COL_RETURN = [
    CategoriesSchema.code, CategoriesSchema.category_name, CategoriesSchema.sort_priority, CategoriesSchema.category_logo, CategoriesSchema.category_banner, CategoriesSchema.description, CategoriesSchema.description_images, CategoriesSchema.items_list
]

HOMEPAGE_COLLECTION_COL_RETURN = [
    "code", "homepage_collection_name", "images", "logo_images", "tags", "collection_discount", "collection_info", "redirect_to", 
    "redirect_type", "redirect_name", "filters", "products"
]

# PRODUCT_COLLECTION_RETURN = [
#     "collection_code", "collection_name", "sort_priority", "sku_code"
# ]

HOMEPAGE_COL_RETURN = [
    HomepageSchema.code, HomepageSchema.homepage_name, HomepageSchema.component_title, HomepageSchema.component_type, HomepageSchema.component_elements_type, HomepageSchema.component_elements, HomepageSchema.component_rank, HomepageSchema.component_secondary_title, 
    HomepageSchema.widget_redirect_to, HomepageSchema.component_category_link, HomepageSchema.component_background_color, HomepageSchema.ui_specs, HomepageSchema.show_title, HomepageSchema.max_visible_element, HomepageSchema.h1_tag, HomepageSchema.description_tag, HomepageSchema.title_tag
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