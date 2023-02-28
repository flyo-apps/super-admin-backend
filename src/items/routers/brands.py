from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from auth.authentication_user import get_current_active_user
from ..crud.brands import BrandsCollection
from ..models.brands import (
    BrandCreateBaseModel,
    BrandUpdateBaseModel
)
from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/v1/create_brand",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_brand(
    brand_details: BrandCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        brands_collection = BrandsCollection()
        return await brands_collection.create_brand(brand_details=brand_details,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/update_brand",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_brand(
    brand_update_details: BrandUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        brands_collection = BrandsCollection()
        return await brands_collection.update_brand(brand_update_details=brand_update_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/v1/get_all_brands",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_all_brands(
    db: Session = Depends(auroradb.get_db),
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
):
    try:
        brands_collection = BrandsCollection()
        return await brands_collection.get_all_brands(page=page, limit=limit, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/get_brand",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_brand(
    code: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        brands_collection = BrandsCollection()

        return await brands_collection.get_brand(code=code, db=db)

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

#not used in scripts
# @router.get(
#     "/v1/get_brand_with_names_by_title",
#     dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
# )
# async def get_brand_with_names_by_title(
#     brand_title: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.get_brand_with_names_by_title(brand_title=brand_title)

#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.get(
#     "/v1/brand_details_lists",
#     dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
# )
# async def brand_details_lists(
#     brand_id: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         brand_details_lists = await items_wrapper_collection.get_brand_details_lists(brand_id=brand_id)

#         return brand_details_lists

#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/brand/add_subcategory",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def add_brand_subcategory(
#     brand_title: str,
#     subcategory_title: str
# ):
#     try:
#         brands_collection = BrandsCollection()

#         return await brands_collection.add_subcategory(
#             brand_title=brand_title,
#             category_title=subcategory_title
#         )

#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/brand/remove_subcategory",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def remove_brand_subcategory(
#     brand_title: str,
#     subcategory_title: str
# ):
#     try:
#         brands_collection = BrandsCollection()

#         return await brands_collection.remove_subcategory(
#             brand_title=brand_title,
#             category_title=subcategory_title
#         )

#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/brand/add_to_category",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def add_brand_to_category(
#     brand_title: str,
#     category_title: str
# ):
#     try:
#         brands_collection = BrandsCollection()

#         return await brands_collection.add_to_category(
#             brand_title=brand_title,
#             category_title=category_title
#         )

#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/brand/remove_from_category",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def remove_brand_from_category(
#     brand_title: str,
#     category_title: str
# ):
#     try:
#         brands_collection = BrandsCollection()

#         return await brands_collection.remove_from_category(
#             brand_title=brand_title,
#             category_title=category_title
#         )

#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/brand/add_product_to_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def add_product_to_brand_list(
#     brand_title: str,
#     flyo_sku_code: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.add_product_to_brand_list(
#             brand_title=brand_title,
#             flyo_sku_code=flyo_sku_code,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/brand/remove_product_from_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def remove_product_from_brand_list(
#     brand_title: str,
#     flyo_sku_code: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.remove_product_from_brand_list(
#             brand_title=brand_title,
#             flyo_sku_code=flyo_sku_code,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/brand/add_product_type_to_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def add_product_type_to_brand_list(
#     brand_title: str,
#     product_type: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.add_product_type_to_brand_list(
#             brand_title=brand_title,
#             product_type=product_type,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/brand/remove_product_type_from_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def remove_product_type_from_brand_list(
#     brand_title: str,
#     product_type: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.remove_product_type_from_brand_list(
#             brand_title=brand_title,
#             product_type=product_type,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/brand/add_filter_to_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def add_filter_to_brand_list(
#     brand_title: str,
#     filter_name: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.add_filter_to_brand_list(
#             brand_title=brand_title,
#             filter_name=filter_name,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/brand/remove_filter_from_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def remove_filter_from_brand_list(
#     brand_title: str,
#     filter_name: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.remove_filter_from_brand_list(
#             brand_title=brand_title,
#             filter_name=filter_name,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/delete_brand",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_brand(
    code: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        brands_collection = BrandsCollection()

        return await brands_collection.delete_brand(code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


# @router.get(
#     "/v1/search_brand",
#     dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
# )
# async def search_brand(
#     search_keyword: str,
#     db: Session = Depends(auroradb.get_db),
# ):
#     try:
#         brands_collection = BrandsCollection()
#         return await brands_collection.search_brand(db=db, search_keyword=search_keyword)
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/create_brand_store",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_brand_store(
    brand_name: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        brands_collection = BrandsCollection()
        return await brands_collection.create_brand_store(db=db, brand_name=brand_name)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/remove_brand_store",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def remove_brand_store(
    brand_name: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        brands_collection = BrandsCollection()
        return await brands_collection.remove_brand_store(db=db, brand_name=brand_name)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
