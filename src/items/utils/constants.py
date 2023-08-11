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
    "Product", "Brand", "Category", "HomepageCollection", "BrandCollection", "Refer", "Filter", "ProductCollection", "Homepage", "Story", "Blog", "IfStore", "Redirection", "MultiStory"
]

VALID_REDIRECTION_ELEMENT_TYPE = ["homepage", "refer", "giftcards", "cart", "wishlist", "blogs", "about", "help", "wallet", "address", "occasion"]

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
QUICK_BANNER_MAIN_KEY = "QUICK_BANNER"

PRODUCTS_COL_RETURN_LIST = [
    ProductsSchema.code, ProductsSchema.sku_code, ProductsSchema.product_name, ProductsSchema.discount, ProductsSchema.mrp, ProductsSchema.list_price, ProductsSchema.brand, ProductsSchema.media, ProductsSchema.product_tag, ProductsSchema.fine_fashion_tag, ProductsSchema.category1
]

SORTING_LIST = [
    "Popularity", "What's New", "Price - Low to High", "Price - High to Low", "Discount - Low to High", "Discount - High to Low"
]

FILTER_MAP = {
    "collection": {"group_by": "collection, collection2, collection3, collection4", "order_by": "collection, collection2, collection3, collection4", "select_statement": "collection, collection2, collection3, collection4, count(*)"},
    "category": {"group_by": "category1, category2, category3", "order_by": "category1", "select_statement": "category1, category2, category3, count(*)"}, 
    "product_type": {"group_by":"product_type1, product_type2, product_type3", "order_by": "product_type1", "select_statement": "product_type1, product_type2, count(*)"}, 
    "occasion": {"group_by":"usecase1, usecase2, usecase3, usecase4, usecase5", "order_by": "usecase1,usecase2,usecase3", "select_statement": "usecase1, usecase2, usecase3, usecase4, usecase5, count(1)"}, 
    "gender": {"group_by":"gender", "order_by": "gender", "select_statement": "gender , count(*)"}, 
    "price": {"group_by": None, "order_by": None, "select_statement": "MAX(list_price), MIN(list_price)"}, 
    "brand":{"group_by": "brand", "order_by": "brand", "select_statement": "brand , count(*)"}, 
    "design_type":{"group_by": "design_type", "order_by": "design_type", "select_statement": "design_type , count(*)"}, 
    "size": {"group_by":"size", "order_by": "size", "select_statement": "size , count(*)"}, 
    "discount": {"group_by":"discount_range", "order_by": None,"select_statement": "case when discount >= .1 and discount < .2 then '10 and above' when discount >= .2 and discount < .3 then '20 and above' when discount >= .3 and discount < .4 then '30 and above' when discount >= .4 and discount < 0.5 then '40 and above' when discount >= .5 and discount < .6 then '50 and above' when discount >= .6 and discount < .7 then '60 and above' when discount >= .7 and discount < 1 then '70 and above' else 'OTHERS' end as discount_range, count(1) as Count"}, 
    "metal": {"group_by":"metal1, metal2, metal3", "order_by": "metal1, metal2, metal3", "select_statement": "metal1, metal2, metal3, count(*) "}, 
    "material": {"group_by":"material1, material2, material3", "order_by": "material1, material2, material3", "select_statement": "material1, material2, material3, count(*) "}, 
    # "stone": {"group_by":"stone1, stone2, stone3", "order_by": "stone1, stone2, stone3", "select_statement": "stone1, stone2, stone3, count(*) "}, 
    "colour": {"group_by":"colour1, colour2, colour3", "order_by": "colour1, colour2, colour3", "select_statement": "colour1, colour2, colour3 , count(*)"},
    "metal_colour": {"group_by":"metal_colour1, metal_colour2, metal_colour3", "order_by": "metal_colour1, metal_colour2, metal_colour3", "select_statement": "metal_colour1, metal_colour2, metal_colour3 , count(*)"},
    # "style_of_jewellery": {"group_by":"style_of_jewellery", "order_by": "style_of_jewellery", "select_statement": "style_of_jewellery , count(*)"}, 
    "plating": {"group_by":"plating", "order_by": "plating", "select_statement": "plating, count(*)"}, 
    "warranty":{"group_by": "warranty", "order_by": None,"select_statement": "warranty, count(*) "}, 
    "shipping_time": {"group_by":"shipping_time", "order_by": "shipping_time", "select_statement": "shipping_time, count(*)"}, 
    "purity": {"group_by":"purity", "order_by": "purity", "select_statement": "purity , count(*)"}, 
    # "designer": {"group_by":"designer", "order_by": "designer", "select_statement": "designer , count(*)"}, 
    "gifting": {"group_by":"gifting", "order_by": None,"select_statement": "gifting, count(*) "}, 
    # "virtual_try_on": {"group_by":"virtual_try_on", "order_by": None,"select_statement": "virtual_try_on , count(*)"}
}