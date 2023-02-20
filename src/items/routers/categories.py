
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from auth.authentication_user import get_current_active_user
from ..crud.categories import CategoriesCollection
from ..models.categories import (
    CategoryCreateBaseModel,
    CategoryUpdateBaseModel
)

from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/v1/create_category",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_category(
    category_details: CategoryCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.create_category(category_details=category_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/update_category",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_category(
    category_update_details: CategoryUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.update_category(category_update_details=category_update_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/v1/get_all_categories",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_all_categories(
    db: Session = Depends(auroradb.get_db),
    page: Optional[int] = 1,
    limit: Optional[int] = 30,
):
    try:
        categories_collection = CategoriesCollection()
        return await categories_collection.get_all_categories(db=db, limit=limit, page=page)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/v1/get_all_categories_lists",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_all_categories_lists(
    parent_category: Optional[str] = None
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.get_all_categories_lists()

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/v1/get_category",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_category(
    category_code: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.get_category(db=db, category_code=category_code)

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

#not used in python script

# @router.get(
#     "/v1/get_category_with_names_by_title",
#     dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
# )
# async def get_category_with_names_by_title(
#     category_title: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.get_category_with_names_by_title(title=category_title)

#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.get(
#     "/v1/category_details_lists",
#     dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
# )
# async def category_details_lists(
#     category_id: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         category_details_lists = await items_wrapper_collection.get_category_details_lists(category_id=category_id)

#         return category_details_lists

#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/make_root_category",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def make_root_category(
#     category_id: str
# ):
#     try:
#         categories_collection = CategoriesCollection()

#         return await categories_collection.make_root_category(
#             category_id=category_id
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/make_subcategory",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def make_subcategory(
#     category_title: str,
#     parent_title: str
# ):
#     try:
#         categories_collection = CategoriesCollection()

#         return await categories_collection.make_subcategory(
#             category_title=category_title,
#             parent_title=parent_title
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/category/add_product_to_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def add_product_to_category_list(
#     category_title: str,
#     flyo_sku_code: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.add_product_to_category_list(
#             category_title=category_title,
#             flyo_sku_code=flyo_sku_code,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/category/remove_product_from_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def remove_product_from_category_list(
#     category_title: str,
#     flyo_sku_code: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.remove_product_from_category_list(
#             category_title=category_title,
#             flyo_sku_code=flyo_sku_code,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/category/add_brand_to_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def add_brand_to_category_list(
#     category_title: str,
#     brand_title: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.add_brand_to_category_list(
#             category_title=category_title,
#             brand_title=brand_title,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/category/remove_brand_from_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def remove_brand_from_category_list(
#     category_title: str,
#     brand_title: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.remove_brand_from_category_list(
#             category_title=category_title,
#             brand_title=brand_title,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/category/add_product_type_to_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def add_product_type_to_category_list(
#     category_title: str,
#     product_type: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.add_product_type_to_category_list(
#             category_title=category_title,
#             product_type=product_type,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/category/remove_product_type_from_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def remove_product_type_from_category_list(
#     category_title: str,
#     product_type: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.remove_product_type_from_category_list(
#             category_title=category_title,
#             product_type=product_type,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/category/add_filter_to_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def add_filter_to_category_list(
#     category_title: str,
#     filter_name: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.add_filter_to_category_list(
#             category_title=category_title,
#             filter_name=filter_name,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


# @router.post(
#     "/v1/category/remove_filter_from_list",
#     dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
# )
# async def remove_filter_from_category_list(
#     category_title: str,
#     filter_name: str,
#     list_name: str
# ):
#     try:
#         items_wrapper_collection = ItemsWrapperCollection()

#         return await items_wrapper_collection.remove_filter_from_category_list(
#             category_title=category_title,
#             filter_name=filter_name,
#             list_name=list_name
#         )
#     except Exception:
#         raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/delete_category",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_category(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.delete_category(code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/disable_category",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def disable_category(
    category_id: str
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.disable_category(
            category_id=category_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/v1/search_category",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def search_category(
    search_keyword: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        categories_collection = CategoriesCollection()

        return await categories_collection.search_category(db=db, search_keyword = search_keyword)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
