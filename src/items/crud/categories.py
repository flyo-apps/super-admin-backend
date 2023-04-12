from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from ..utils.constants import CATEGORY_COL_RETURN
from db.mongo.mongo_model import OID
from ..models.categories import (
    CreateCategoryFullModelOut,
    CategoryCreateBaseModel,
    CategoryCreateModel,
    CategoryUpdateBaseModel,
    CategoryUpdateModel,
    CategoryDeleteModel
)
from ..schemas.categories import (
    CategoriesSchema
)
from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session

class CategoriesCollection:
    def __init__(self):
        self.model = CRUDBase(CategoriesSchema)


    async def create_category(
        self,
        category_details: CategoryCreateBaseModel,
        db: Session
    ) -> any:
        try:
            existing_category = self.model.get_one(db=db, code=category_details.code)
            if existing_category is not None:
                return

            category_create = CategoryCreateModel(**category_details.dict())
            created_brand = self.model.create(db=db, obj_in=category_create)

            return created_brand if created_brand else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def update_category(
        self,
        category_update_details: CategoryUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            category = self.model.get_one(db=db, code=category_update_details.code)
            if category == None:
                return {"internal_response_code": 1, "category_code": category_update_details.code, "message": "Category not found"}

            category_update = CategoryUpdateModel(**category_update_details.dict(exclude_unset=True))
            category_update.is_updated = True
            category_update.updated_at = datetime.now()
            updated_category = self.model.update(db=db, db_obj=category,obj_in=category_update)
            return {"internal_response_code": 0, "category_code": category_update_details.code, "message": "Category updated"} if updated_category else {"internal_response_code": 1, "category_code": category_update_details.code, "message": "Product not updated"}
            
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def update_parent_category(
        self,
        category_id: str,
        subcategory_id: str
    ) -> any:
        try:
            if category_id is None or subcategory_id is None:
                return

            updater = {
                    "$addToSet": {
                        "subcategories": subcategory_id
                    }
                }

            finder = {"_id": ObjectId(category_id)}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def update_parent_category_on_remove(
        self,
        category_id: str,
        removed_id: str
    ) -> any:
        try:
            if category_id is None or removed_id is None:
                return

            updater = {
                    "$pull": {
                        "subcategories": removed_id
                    }
                }

            finder = {"_id": ObjectId(category_id)}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_all_categories(
        self,
        page: int,
        limit: int,
        db: Session
    ) -> any:
        try:
            if page == 1:
                skip = 0
            else:
                skip = (page - 1)*limit
            
            where_clause = "(is_deleted=False)"
            data = self.model.get_all(db=db, column_load=CATEGORY_COL_RETURN, where_clause=where_clause, skip=skip, limit=limit)
            return data if data else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_all_categories_lists(self) -> any:
        try:
            categories = await self.get_all_categories()

            categories_lists = []

            for category in categories:
                subcategories = await self.get_details_from_ids(category.subcategories)
                categories_lists.append({"category": category, "subcategories": subcategories})

            return categories_lists if categories_lists else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_all_subcategories(
        self,
        parent_category: str
    ) -> any:
        try:
            sort = [("sort_priority_category", -1)]
            filter_condition = {"is_deleted": False, "is_disabled": False, "is_subcategory": True, "parent_category": parent_category}
            data = await self.collection.find(
                finder=filter_condition,
                sort=sort,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
            )

            return data if data else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_details_from_ids(
        self,
        category_ids: List[OID]
    ) -> any:
        try:
            if not category_ids:
                return None

            if len(category_ids) > 0:
                filter_condition = {"_id": {"$in": category_ids}, "is_deleted": False, "is_disabled": False}

                category_details = await self.collection.find(
                    finder=filter_condition,
                    return_doc_id=True,
                    extended_class_model=CreateCategoryFullModelOut,
                )

                return category_details if category_details else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_names_from_ids(
        self,
        category_ids: List[OID]
    ) -> any:
        try:
            if not category_ids:
                return None

            if len(category_ids) > 0:
                filter_condition = {"_id": {"$in": category_ids}, "is_deleted": False, "is_disabled": False}

                category_details = await self.collection.find(
                    finder=filter_condition,
                    return_doc_id=True,
                    extended_class_model=CreateCategoryFullModelOut,
                )

                category_names = []
                for category_detail in category_details:
                    category_names.append(category_detail.title)

                return category_names
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_category_by_id(
        self,
        category_id: str
    ) -> any:
        try:
            finder = {"_id": ObjectId(category_id)}

            category = await self.collection.find_one(
                finder=finder,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut
            )

            return category if category else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_category(
        self,
        category_code: str,
        db: Session
    ) -> any:
        try:
            category = self.model.get_one(db=db, code=category_code, column_load=CATEGORY_COL_RETURN)
            return category if category else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_category_by_name(
        self,
        db: Session,
        name: str
    ) -> any:
        try:

            where_clause = f"""category_name='{name}'"""
            category = self.model.get_one(db=db, where_clause=where_clause)
            
            return category if category else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def make_root_category(
        self,
        category_id: str
    ) -> any:
        try:
            category_data = await self.collection.find_one(
                    {"_id": ObjectId(category_id)},
                    return_doc_id=True,
                    extended_class_model=CreateCategoryFullModelOut,
                )

            if category_data is not None and category_data.parent_category is not None:
                await self.update_parent_category_on_remove(category_id=category_data.parent_category, removed_id=category_id)

            finder = {"_id": ObjectId(category_id)}
            updater = {"$set": {"is_subcategory": False, "parent_category": None}}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def make_subcategory(
        self,
        category_title: str,
        parent_title: str
    ) -> any:
        try:
            category_data = await self.get_category_by_title(title=category_title)
            parent_category_data = await self.get_category_by_title(title=parent_title)

            if category_data is not None and parent_category_data is not None:
                if category_data.parent_category is not None:
                    await self.update_parent_category_on_remove(category_id=category_data.parent_category, removed_id=str(category_data.id))
                
                await self.update_parent_category(category_id=parent_category_data.id, subcategory_id=str(category_data.id))

            finder = {"_id": ObjectId(category_data.id)}
            updater = {"$set": {"is_subcategory": True, "parent_category": str(parent_category_data.id)}}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    

    async def add_brand_to_category_title(
        self,
        title: str,
        brand_id: str
    ) -> any:
        try:
            finder = {"title": title}
            updater = {
                "$addToSet": {
                    "brands": brand_id
                }
            }

            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def remove_brand_from_category_title(
        self,
        title: str,
        brand_id: str
    ) -> any:
        try:
            finder = {"title": title}
            updater = {
                "$pull": {
                    "brands": brand_id
                }
            }

            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_db_list_name(
        self,
        list_name: str
    ) -> any:
        try:
            if list_name == "top_products":
                return "top_products"
            elif list_name == "new_products":
                return "new_products"
            elif list_name == "trending_products":
                return "trending_products"
            elif list_name == "discounted_products":
                return "discounted_products"
            elif list_name == "brands":
                return "brands"
            elif list_name == "top_brands":
                return "top_brands"
            elif list_name == "new_brands":
                return "new_brands"
            elif list_name == "product_types":
                return "product_types"
            elif list_name == "filters":
                return "filters"
            elif list_name == "subcategories":
                return "subcategories"
            else:
                return None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_ui_list_name(
        self,
        list_name: str
    ) -> any:
        try:
            if list_name == "top_products":
                return "Top Products"
            elif list_name == "new_products":
                return "New Products"
            elif list_name == "trending_products":
                return "Trending Products"
            elif list_name == "discounted_products":
                return "Discounted Products"
            elif list_name == "brands":
                return "Brands"
            elif list_name == "top_brands":
                return "Top Brands"
            elif list_name == "new_brands":
                return "New Brands"
            elif list_name == "product_types":
                return "Product Types"
            elif list_name == "filters":
                return "Filters"
            elif list_name == "subcategories":
                return "Sub Categories"
            else:
                return None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_list_item_type(
        self,
        list_name: str
    ) -> any:
        try:
            if list_name == "top_products":
                return "product"
            elif list_name == "new_products":
                return "product"
            if list_name == "trending_products":
                return "product"
            elif list_name == "discounted_products":
                return "product"
            elif list_name == "brands":
                return "brand"
            elif list_name == "top_brands":
                return "brand"
            elif list_name == "new_brands":
                return "brand"
            elif list_name == "product_types":
                return "product_type"
            elif list_name == "filters":
                return "filter"
            elif list_name == "subcategories":
                return "category"
            else:
                return None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def add_item_to_category_list(
        self,
        category_title: str,
        item_id: OID,
        list_name: str
    ) -> any:
        try:
            db_list_name = await self.get_db_list_name(list_name=list_name)
            if db_list_name is None:
                return

            finder = {"title": category_title}
            updater = {
                "$addToSet": {
                    db_list_name: item_id
                }
            }

            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def remove_item_from_category_list(
        self,
        category_title: str,
        item_id: OID,
        list_name: str
    ) -> any:
        try:
            db_list_name = await self.get_db_list_name(list_name=list_name)
            if db_list_name is None:
                return

            finder = {"title": category_title}
            updater = {
                "$pull": {
                    db_list_name: item_id
                }
            }

            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def remove_brand_from_category_id(
        self,
        category_id: str,
        brand_id: str
    ) -> any:
        try:
            finder = {"_id": category_id}
            updater = {
                "$pull": {
                    "brands": brand_id
                }
            }

            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
                insert_if_not_found=False,
                return_updated_document=True,
            )

            return result

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def delete_category(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            category_delete = CategoryDeleteModel(code=code)
            category_delete_dict = category_delete.dict()
            category = self.model.get_one(db=db, code=code)
            if category == None:
                {"internal_response_code": 1, "code": code, "message": "Category not found"}
            deleted_category = self.model.update(db=db, db_obj=category,obj_in=category_delete_dict)

            return {"internal_response_code": 0, "code": code, "message": "Category deleted"} if deleted_category else {"internal_response_code": 1, "code": code, "message": "Category not deleted"} 
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def disable_category(
        self,
        category_id: str
    ) -> any:
        try:
            category_data = await self.collection.find_one(
                    {"_id": ObjectId(category_id)},
                    return_doc_id=True,
                    extended_class_model=CreateCategoryFullModelOut,
                )

            if category_data is not None and category_data.parent_category is not None:
                await self.update_parent_category_on_remove(category_id=category_data.parent_category, removed_id=category_id)

            finder = {"_id": ObjectId(category_id)}
            updater = {"$set": {"is_disabled": True, "disabled_on": datetime.now()}}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CreateCategoryFullModelOut,
                insert_if_not_found=False,
                return_updated_document=True
            )

            return result
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    
    async def search_category(
        self,
        search_keyword: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""(array_to_string(search_tags, ',') ~* '{search_keyword}' or category_name ~* '{search_keyword}') AND is_deleted=false"""
            sorting_method = "sort_priority DESC"
            search_data = self.model.get_all(db=db, where_clause=where_clause, column_load=CATEGORY_COL_RETURN, sorting_method=sorting_method)
            return {"internal_response_code": 0, "message": "success", "data": search_data} if search_data else {"internal_response_code": 1, "message": "success", "data": search_data}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def get_all_categories_projection(
        self,
        limit: Optional[int] = 30,
        page: Optional[int] = 1
    ) -> any:
        try:
            if page == 1:
                skip = 0
            if page > 1:
                skip = limit*(page-1)
            return await self.collection.find(
                finder={
                    "is_deleted": False, 
                    "is_disabled": False
                },
                projection={
                    "title" : 1,
                    "product_types": 1
                },
                skip=skip
            )
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    

    