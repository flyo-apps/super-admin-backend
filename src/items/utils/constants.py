from ..schemas.homepage import HomepageSchema
from ..schemas.categories import CategoriesSchema
from ..schemas.brands_collection import BrandsCollectionSchema
from ..schemas.brands import BrandsSchema
from ..schemas.product_collection import ProductCollectionItemsSchema
from ..schemas.homepage_group import HomePageCollectionsSchema
from ..schemas.products import ProductsSchema
from ..schemas.usecases import UsecasesSchema

BRANDS_COL_RETURN = [
    BrandsSchema.code, BrandsSchema.brand_name, BrandsSchema.sort_priority, BrandsSchema.logo_image, BrandsSchema.banner_image, BrandsSchema.description, BrandsSchema.description_images, BrandsSchema.items_list, BrandsSchema.search_tags
]

BRANDS_COLLECTION_COL_RETURN = [
    BrandsCollectionSchema.code, BrandsCollectionSchema.brand_collection_name, BrandsCollectionSchema.sort_priority, BrandsCollectionSchema.brand_name, BrandsCollectionSchema.collection_logo, BrandsCollectionSchema.collection_banner, BrandsCollectionSchema.description, BrandsCollectionSchema.description_images,
    BrandsCollectionSchema.items_list, BrandsCollectionSchema.search_tags
]

PRODUCT_ITEMS_COL_RETURN = [
    ProductsSchema.code, ProductsSchema.sku_code, ProductsSchema.media, ProductsSchema.discount, ProductsSchema.mrp, ProductsSchema.list_price, ProductsSchema.brand, ProductsSchema.product_name, ProductsSchema.vendor_code, ProductsSchema.product_tag, ProductsSchema.fine_fashion_tag,
    ProductsSchema.viewing_or_bought, ProductsSchema.size, ProductsSchema.category1, ProductsSchema.product_type1, ProductsSchema.pickup_city, ProductsSchema.pick_pack_time
]

CATEGORY_COL_RETURN = [
    CategoriesSchema.code, CategoriesSchema.category_name, CategoriesSchema.sort_priority, CategoriesSchema.category_logo, CategoriesSchema.category_banner, CategoriesSchema.description, CategoriesSchema.description_images, CategoriesSchema.items_list
]

HOMEPAGE_COLLECTION_COL_RETURN = [
    HomePageCollectionsSchema.code, HomePageCollectionsSchema.homepage_collection_name, HomePageCollectionsSchema.images, HomePageCollectionsSchema.logo_images, HomePageCollectionsSchema.tags, HomePageCollectionsSchema.collection_discount, HomePageCollectionsSchema.collection_info, HomePageCollectionsSchema.redirect_to,
    HomePageCollectionsSchema.redirect_type, HomePageCollectionsSchema.redirect_name, HomePageCollectionsSchema.filters, HomePageCollectionsSchema.products
]

PRODUCT_COLLECTION_RETURN = [
    ProductCollectionItemsSchema.collection_code, ProductCollectionItemsSchema.collection_name, ProductCollectionItemsSchema.sort_priority, ProductCollectionItemsSchema.sku_code
]

HOMEPAGE_COL_RETURN = [
    HomepageSchema.code, HomepageSchema.homepage_name, HomepageSchema.component_title, HomepageSchema.component_type, HomepageSchema.component_elements_type, HomepageSchema.component_elements, HomepageSchema.component_rank, HomepageSchema.component_secondary_title, 
    HomepageSchema.widget_redirect_to, HomepageSchema.component_category_link, HomepageSchema.component_background_color, HomepageSchema.ui_specs, HomepageSchema.show_title, HomepageSchema.max_visible_element, HomepageSchema.h1_tag, HomepageSchema.description_tag, HomepageSchema.title_tag
]

VALID_COMPONENT_TYPES = ["FWBanner", "FWImageCarousel", "FWITRCarousel", "FWITLCarousel", "BrandCard1", "BrandCard2", "CollectionCard1", "CollectionCard2", 
    "Product", "UsecaseList6", "ITOverlayCircle", "ITOverlaySquare", "ITOverlayCircle6", "CircleList", "FeaturedList4", "FilterChipList", "FilterImageList", 
    "ChipListSingle", "ChipListMulti", "VerticalList" 
]

VALID_COMPONENT_ELEMENTS_TYPE = [
    "Product", "Brand", "Category", "HomepageCollection", "BrandCollection", "Refer", "Filter", "ProductCollection", "Homepage", "Story", "Blog", "Store"
]

VALID_ADD_TO_LIST = [
    "Brand", "BrandCollection", "Category", "Usecase", "Homepage"
]

VALID_HOMEPAGE_COMPONENT_NAMES_FOR_PAGES = [
   "Homepage_Brand", "Homepage_BrandCollection", "Homepage_Category", "Homepage_Usecase", "Homepage_Homepage"
]

PRODUCT_LIMIT = 30

USECASE_COL_RETURN = [UsecasesSchema.code, UsecasesSchema.usecase_name, UsecasesSchema.sort_priority, UsecasesSchema.usecase_logo, UsecasesSchema.usecase_banner, UsecasesSchema.description, UsecasesSchema.description_images, UsecasesSchema.items_list, UsecasesSchema.search_tags]

RECENTLY_VIEWED_PRODUCT = 'RVP'
QUICK_FILTER_MAIN_KEY = "QUICK_FILTER"