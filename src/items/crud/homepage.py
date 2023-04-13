from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, BackgroundTasks
from .categories import CategoriesCollection
from .brands import BrandsCollection
from .products import ProductsCollection
from .stories import StoriesCollection
import json
from .homepage_group import HomepageGroupCollection
from .brands_collection import BrandsCollectionCollection
from .product_collection import ProductCollectionCollection
from ..utils.constants import (
    HOMEPAGE_COL_RETURN, VALID_COMPONENT_TYPES, VALID_COMPONENT_ELEMENTS_TYPE, VALID_ADD_TO_LIST, VALID_HOMEPAGE_COMPONENT_NAMES_FOR_PAGES
)
from ..models.homepage import (
    HomePageDeleteModel,
    HomePageElementsBaseUpdateModel,
    HomePageElementsUpdateModel,
    HomePageCreateBaseModel,
    HomePageCreateModel,
    HomePageUpdateBaseModel,
    HomePageUpdateModel
)
import copy
from ..schemas.homepage import HomepageSchema
from sqlalchemy.orm import Session
from db.aurora.aurora_base import CRUDBase
from db.redis.redis_base import RedisBase

class HomePageCollection:
    def __init__(self):
        self.model = CRUDBase(HomepageSchema)
        self.redis = RedisBase()

    async def create_homepage_component(
        self,
        homepage_details: HomePageCreateBaseModel,
        username: str,
        db: Session,
        background_tasks: BackgroundTasks,
        from_lambda: Optional[bool] = False,
    ) -> any:
        try:
            details = await self.get_homepage_by_homepage_name_and_component_title(db=db, code=homepage_details.code ,homepage_name=homepage_details.homepage_name, component_title=homepage_details.component_title)
            if details:
                return {"internal_response_code": 1, "message": "component already exists"}

            if homepage_details.component_type not in VALID_COMPONENT_TYPES:
                return {"internal_response_code": 1,"message": f"""Provide correct component type"""}
                    
            if homepage_details.component_elements_type not in VALID_COMPONENT_ELEMENTS_TYPE:
                return {"internal_response_code": 1,"message": f"""Provide correct component elements type"""}

            component_category_link_id = None

            if homepage_details.component_category_link is not None:
                categories_collection = CategoriesCollection()
                category_details = await categories_collection.get_category_by_name(db=db, name=homepage_details.component_category_link)

                if category_details is not None:
                    component_category_link_id = category_details.code
                    homepage_details.component_category_link = component_category_link_id
                else:
                    return {"internal_response_code": 1, "message": f"""Category with Title: {homepage_details.component_category_link}, not found"""}
            
            # if from_lambda == False and insert_id:
            #     homepage_lambda_collection = HomePageLambdaCollection()
            #     data = {
            #         "user_id": username,
            #         "environ": os.environ.get("ENV"),
            #         "api_params": {
            #             "api_url": "/v1/create_homepage_component",
            #             "homepage_title": homepage_title,
            #             "component_title": component_title,
            #             "component_type" : component_type,
            #             "component_elements_type" : component_elements_type,
            #             "component_rank" : component_rank,
            #             "component_secondary_title": component_secondary_title,
            #             "widget_redirect_to": widget_redirect_to,
            #             "component_category_link" : component_category_link,
            #             "component_background_color": component_background_color
            #         }   
            #     }
            #     background_tasks.add_task(homepage_lambda_collection.update_and_create_for_all_locations, data=data)
                # await homepage_lambda_collection.update_and_create_for_all_locations(data=data)
            home_page_create = HomePageCreateModel(**homepage_details.dict(exclude_unset=True))
            created_home_page = self.model.create(db=db, obj_in=home_page_create)

            return {"internal_response_code": 0, "message": "success", "data": created_home_page} if created_home_page else {"internal_response_code": 1, "message": "success", "data": None}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_homepage_details(
        self,
        homepage_name: str,
        db: Session,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        refresh_redis: Optional[bool] = True
    ) -> any:
        try:
            if refresh_redis == True:
                start = (page -1) * limit
                if page > 1:
                    start = start +1
                end = (page) * limit
                data = await self.redis.lrange(homepage_name, start, end)
                final_data = []
                if data:
                    for each_data in data:
                        final_data.append(json.loads(each_data))
                
                if page == 1 and len(final_data) == 0:
                    pass
                else:
                    return final_data

            where_clause = f"""(homepage_name = '{homepage_name}') AND (is_deleted= False)"""
            sorting_method = "component_rank"
            if limit ==  None and page == None:
                skip = 0
                page = 1
                limit = 30
            else:
                if page == 1:
                    skip = 0
                elif page > 1:
                    skip = (page -1)*limit

            data = self.model.get_all(db=db, where_clause=where_clause, skip=skip, limit=limit, sorting_method=sorting_method, column_load=HOMEPAGE_COL_RETURN)

            return data if data else []
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def get_homepage_component_by_component_title(
        self,
        component_title: str,
        db: Session,
    ) -> any:
        try:
            where_clause = f"""(component_title = '{component_title}')"""
            data = self.model.get_one(db=db, where_clause=where_clause, column_load=HOMEPAGE_COL_RETURN)

            return data if data else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def get_homepage_component_by_component_title_and_code(
        self,
        component_title: str,
        code: str,
        db: Session,
    ) -> any:
        try:
            where_clause = f"""(component_title = '{component_title}') AND (code='{code}')"""
            data = self.model.get_one(db=db, where_clause=where_clause, column_load=HOMEPAGE_COL_RETURN)

            return data if data else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_homepage_by_homepage_name_and_component_title(
        self,
        db: Session,
        homepage_name: str,
        component_title: str,
        code: Optional[str] = None,
    ) -> any:
        try:
            if code==None:
                where_clause = f"""(homepage_name='{homepage_name}') AND (component_title='{component_title}')"""
            else:
                 where_clause = f"""(homepage_name='{homepage_name}' AND component_title='{component_title}') OR (code='{code}')"""

            details = self.model.get_one(db=db, where_clause=where_clause, column_load=HOMEPAGE_COL_RETURN)

            return details if details else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    
    async def get_homepage_component_by_element_type(
        self,
        homepage_name: str,
        db: Session,
        component_elements_type: str,
        limit: int,
        page: int
    ) -> any:
        try:
            where_clause = f"""((homepage_name='{homepage_name}') AND (component_elements_type='{component_elements_type}') AND (is_deleted=False))"""
            sorting_method = "component_rank"
            if limit ==  None and page == None:
                skip = 0
                page = 1
                limit = 30
            else:
                if page == 1:
                    skip = 0
                elif page > 1:
                    skip = (page -1)*limit
            
            data = self.model.get_all(db=db, where_clause=where_clause, limit=limit, skip=skip, sorting_method=sorting_method)

            return data if data else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_component_element_details_required(
        self,
        component_details_full: any,
        component_elements_type: str
    ) -> any:
        try:
            component_details = {}
            if component_elements_type == 'Category':
                component_details['code'] = component_details_full.code
                component_details['description'] = component_details_full.description
                component_details['category_name'] = component_details_full.category_name
                component_details['description_images'] = component_details_full.description_images
                component_details['category_logo'] = component_details_full.category_logo
            elif component_elements_type == 'Brand':
                component_details['code'] = component_details_full.code
                component_details['brand_name'] = component_details_full.brand_name
                component_details['description'] = component_details_full.description
                component_details['description_images'] = component_details_full.description_images
                component_details['logo_image'] = component_details_full.logo_image
                component_details['has_store'] = component_details_full.has_store
            elif component_elements_type == 'Product':
                component_details['product_name'] = component_details_full["data"].product_name
                component_details['media'] = component_details_full["data"].media
                component_details['brand'] = component_details_full["data"].brand
                component_details['sku_code'] = component_details_full["data"].sku_code
                component_details['code'] = component_details_full["data"].code
                component_details['size'] = component_details_full["data"].size
                component_details['mrp'] = component_details_full["data"].mrp
                component_details['list_price'] = component_details_full["data"].list_price
                component_details['category1'] = component_details_full["data"].category1
                component_details['product_type1'] = component_details_full["data"].product_type1
            elif component_elements_type == "Refer":
                component_details = component_details_full
            elif component_elements_type == "Homepage":
                component_details = component_details_full
            elif component_elements_type == "HomepageCollection":
                component_details_full_dict = component_details_full.__dict__
                del component_details_full_dict["_sa_instance_state"]
                component_details =component_details_full_dict
            elif component_elements_type == "BrandCollection":
                component_details_full_dict = component_details_full.__dict__
                del component_details_full_dict["_sa_instance_state"]
                component_details = component_details_full_dict
            elif component_elements_type == "ProductCollection":
                component_details['code'] = component_details_full.code
                component_details['collection_name'] = component_details_full.collection_name
                component_details['collection_details'] = component_details_full.collection_details
                component_details['collection_images'] = component_details_full.collection_images
            elif component_elements_type == "Story":
                component_details['code'] = component_details_full.code
                component_details['description'] = component_details_full.description
                component_details['story_name'] = component_details_full.story_name
                component_details['story_image'] = component_details_full.story_image
                component_details['redirection_type'] = component_details_full.redirection_type
                component_details['redirection_text'] = component_details_full.redirection_text
                component_details['redirection_value'] = component_details_full.redirection_value
                component_details['filters'] = component_details_full.filters

            else:
                component_details = component_details_full.dict()

            return component_details if component_details else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_component_element_details(
        self,
        db: Session,
        component_elements_type: str,
        component_elements: str,
        filter_details: Optional[dict] = None
    ) -> any:
        try:
            if component_elements_type == "Filter":
                if filter_details == None:
                    return None
                filter_details["title"] = component_elements
                return filter_details 
            elif component_elements_type == "Product":
                products_collection = ProductsCollection()
                component_details_full = await products_collection.get_product_by_sku_code(db=db, sku_code=component_elements)
            elif component_elements_type == "ProductCollection":
                products_collection_collection = ProductCollectionCollection()
                component_details_full = await products_collection_collection.get_collection_detail_by_code(db=db, code=component_elements)
            elif component_elements_type == "Brand":
                brands_collection = BrandsCollection()
                component_details_full = await brands_collection.get_brand(db=db, code=component_elements)
            elif component_elements_type == "Category":
                categories_collection = CategoriesCollection()
                component_details_full = await categories_collection.get_category(db=db, category_code=component_elements)
            elif component_elements_type == "HomepageCollection":
                homepage_group_collection = HomepageGroupCollection()
                component_details_full = await homepage_group_collection.get_homepage_collection_by_name(db=db, name=component_elements)
            elif component_elements_type == "BrandCollection":
                brand_collections_collection = BrandsCollectionCollection()
                component_details_full = await brand_collections_collection.get_brand_collection_by_name(db=db, name=component_elements)
            elif component_elements_type == "Refer":
                component_details_full = {"images": [component_elements]}
            elif component_elements_type == "Homepage":
                component_details_full = {"code": component_elements}
            elif component_elements_type == "Story":
                stories_collection = StoriesCollection()
                component_details_full = await stories_collection.get_story_by_code(db=db, story_code=component_elements)
            else:
                component_details_full = {}

            component_details = await self.get_component_element_details_required(component_details_full=component_details_full, component_elements_type=component_elements_type)

            return component_details if component_details else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_component_element_details_for_remove(
        self,
        component_elements_type: str,
        component_elements: str,
        component_list: List
    ) -> any:
        try:
            if component_elements_type == "Product":
                component_details = [component for component in component_list if component['sku_code'] == component_elements]
            
            elif component_elements_type == "ProductCollection":
                component_details = [component for component in component_list if component['code'] == component_elements]

            elif component_elements_type == "Brand":
                component_details = [component for component in component_list if component['code'] == component_elements]
            
            elif component_elements_type == "Filter":
                component_details = [component for component in component_list if component['title'] == component_elements]

            elif component_elements_type == "Category":
                component_details = [component for component in component_list if component['code'] == component_elements]

            elif component_elements_type == "HomepageCollection":
                component_details = [component for component in component_list if component['homepage_collection_name'] == component_elements]
            
            elif component_elements_type == "BrandCollection":
                component_details = [component for component in component_list if component['brand_collection_name'] == component_elements]

            elif component_elements_type == "Refer":
                component_details = [component for component in component_list if component['images'][0] == component_elements]

            elif component_elements_type == "Homepage":
                component_details = [component for component in component_list if component['code'] == component_elements]

            return component_details[0] if component_details else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def update_homepage(
        self,
        current_user: str,
        from_lambda: bool,
        background_tasks: BackgroundTasks,
        db: Session,
        update_details: HomePageUpdateBaseModel
    ) -> any:
        try:
            details = await self.get_homepage_by_homepage_name_and_component_title(db=db, code=update_details.code, homepage_name=update_details.homepage_name, component_title=update_details.component_title)
            if details is None:
                return {"internal_response_code": 1,"message": f"""No component with title `{update_details.component_title}` found"""}

            if update_details.component_type is not None and update_details.component_type not in VALID_COMPONENT_TYPES:
                return {"internal_response_code": 1,"message": f"""Provide correct component type"""}

            if update_details.component_elements_type is not None and update_details.component_elements_type not in VALID_COMPONENT_ELEMENTS_TYPE:
                return {"internal_response_code": 1,"message": f"""Provide correct component elements type"""}

            homepage_update = HomePageUpdateModel(**update_details.dict(exclude_unset=True))
            homepage_update.is_updated = True
            homepage_update.updated_at = datetime.now()
            homepage_update_dict = homepage_update.dict(exclude_unset=True)
            updated_homepage = self.model.update(db=db, db_obj=details,obj_in=homepage_update_dict)

            if updated_homepage:
                await self.refresh_homepage_redis(db=db, homepage_name=update_details.homepage_name)

            return {"internal_response_code": 0, "component_title": updated_homepage.component_title, "message": "Homepage updated"} if updated_homepage else {"internal_response_code": 1, "component_title": updated_homepage.component_title, "message": "Homepage not updated"}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def update_homepage_elements(
        self,
        db: Session,
        code: str,
        username: str,
        homepage_name: str,
        update_type: str,
        component_title: str,
        component_type: str,
        from_lambda: bool,
        background_tasks: BackgroundTasks,
        component_elements_type: Optional[str] = None,
        component_elements: Optional[str] = None,
        component_elements_image: Optional[str] = None,
        component_elements_secondary_text: Optional[str] = None,
        component_elements_position: Optional[int] = None,
        filter_details: Optional[dict] = None,
        element_background_color: Optional[str] = None
    )-> any:
        try:
            if homepage_name is None or update_type is None or component_title is None or component_type is None:
                return  {"internal_response_code": 1,"message": "failed"}

            details = await self.get_homepage_by_homepage_name_and_component_title(db=db, homepage_name=homepage_name, component_title=component_title, code=code)

            if details is None:
                return {"internal_response_code": 1,"message": f"""No component with title  -`{component_title}` found"""}

            updater = {}

            if update_type == "add_element":
                if component_elements_type is None or component_elements is None:
                    return {"internal_response_code": 1,"message": "failed"}

                if details.component_type == component_type and details.component_elements_type == component_elements_type:

                    component_elements_full = copy.deepcopy(details.component_elements) if copy.deepcopy(details.component_elements) else []

                    component_detail = await self.get_component_element_details(db=db, component_elements_type=component_elements_type, component_elements=component_elements, filter_details=filter_details)

                    if component_detail is not None and component_detail not in component_elements_full:
                        if component_elements_image is not None:
                            component_detail['component_elements_image'] = component_elements_image
                        if component_elements_secondary_text is not None:
                            component_detail['component_elements_secondary_text'] = component_elements_secondary_text
                        if element_background_color is not None:
                            component_detail['element_background_color'] = element_background_color

                        component_elements_full.append(component_detail)
                        updater["component_elements"] = component_elements_full
                    else:
                        return  {"internal_response_code": 1,"message": "failed"}



            elif update_type == "remove_element":
                if component_elements_type is None or component_elements is None:
                    return  {"internal_response_code": 1,"message": "failed"}

                if details.component_type == component_type and details.component_elements_type == component_elements_type:

                    component_elements_full = copy.deepcopy(details.component_elements)
                    
                    component_detail = await self.get_component_element_details_for_remove(component_elements_type=component_elements_type, component_elements=component_elements, component_list=component_elements_full)

                    if component_detail is not None:
                        component_elements_full.remove(component_detail)

                        updater["component_elements"] = component_elements_full
                    else:
                        return  {"internal_response_code": 1,"message": "failed"}
                
                else:
                    return  {"internal_response_code": 1,"message": "failed"}

            elif update_type == "replace_element":
                if component_elements_type is None or component_elements is None or component_elements_position is None:
                    return  {"internal_response_code": 1,"message": "failed"}

                if details.component_type == component_type and details.component_elements_type == component_elements_type:

                    component_elements_full = copy.deepcopy(details.component_elements) if copy.deepcopy(details.component_elements) else []

                    component_detail = await self.get_component_element_details(db=db, component_elements_type=component_elements_type, component_elements=component_elements, filter_details=filter_details)
                    if component_detail is not None and component_detail not in component_elements_full:
                        if component_elements_image is not None:
                            component_detail['component_elements_image'] = component_elements_image
                        if component_elements_secondary_text is not None:
                            component_detail['component_elements_secondary_text'] = component_elements_secondary_text
                        if element_background_color is not None:
                            component_detail['element_background_color'] = element_background_color
                        component_elements_full.pop(component_elements_position)
                        component_elements_full.insert(component_elements_position,component_detail)
                        updater["component_elements"] = component_elements_full
                    else:
                        return  {"internal_response_code": 1,"message": "failed"}
                else:
                    return  {"internal_response_code": 1,"message": "failed"}
                    

            elif update_type == "insert_element":
                if component_elements_type is None or component_elements is None or component_elements_position is None:
                    return  {"internal_response_code": 1,"message": "failed"}

                if details.component_type == component_type and details.component_elements_type == component_elements_type:

                    component_elements_full = copy.deepcopy(details.component_elements) if copy.deepcopy(details.component_elements) else []

                    component_detail = await self.get_component_element_details(db=db, component_elements_type=component_elements_type, component_elements=component_elements)
                    if component_detail is not None and component_detail not in component_elements_full:
                        if component_elements_image is not None:
                            component_detail['component_elements_image'] = component_elements_image
                        if component_elements_secondary_text is not None:
                            component_detail['component_elements_secondary_text'] = component_elements_secondary_text
                        if element_background_color is not None:
                            component_detail['element_background_color'] = element_background_color
                        component_elements_full.insert(component_elements_position,component_detail)
                        updater["component_elements"] = component_elements_full

                    else:
                        return  {"internal_response_code": 1,"message": "failed"}

                else:
                    return  {"internal_response_code": 1,"message": "failed"}

            elif update_type == "change_element_image":

                if component_elements_type is None or component_elements is None or component_elements_image is None:
                    return  {"internal_response_code": 1,"message": "failed"}

                if details.component_type == component_type and details.component_elements_type == component_elements_type:

                    component_elements_full = copy.deepcopy(details.component_elements) if copy.deepcopy(details.component_elements) else []

                    component_detail = await self.get_component_element_details_for_remove(component_elements_type=component_elements_type, component_elements=component_elements, component_list=component_elements_full)

                    if component_detail is not None:
                        component_detail_new = component_detail
                        component_detail_new['component_elements_image'] = component_elements_image

                    component_elements_final = []
                    for component in component_elements_full:
                        if component == component_detail:
                            component_elements_final.append(component_detail_new)
                        else:
                            component_elements_final.append(component)

                    updater["component_elements"] = component_elements_final
                    

            elif update_type == "change_element_secondary_text":

                if component_elements_type is None or component_elements is None or component_elements_secondary_text is None:
                    return  {"internal_response_code": 1,"message": "failed"}

                if details.component_type == component_type and details.component_elements_type == component_elements_type:

                    component_elements_full = copy.deepcopy(details.component_elements) if copy.deepcopy(details.component_elements) else []

                    component_detail = await self.get_component_element_details_for_remove(component_elements_type=component_elements_type, component_elements=component_elements, component_list=component_elements_full)

                    if component_detail is not None:
                        component_detail_new = component_detail
                        component_detail_new['component_elements_secondary_text'] = component_elements_secondary_text

                    component_elements_final = []
                    for component in component_elements_full:
                        if component == component_detail:
                            component_elements_final.append(component_detail_new)
                        else:
                            component_elements_final.append(component)

                    updater["component_elements"] = component_elements_final

            elif update_type == "change_element_background_color":

                if component_elements_type is None or component_elements is None or element_background_color is None:
                    return  {"internal_response_code": 1,"message": "failed"}

                if details.component_type == component_type and details.component_elements_type == component_elements_type:

                    component_elements_full = copy.deepcopy(details.component_elements) if copy.deepcopy(details.component_elements) else []

                    component_detail = await self.get_component_element_details_for_remove(component_elements_type=component_elements_type, component_elements=component_elements, component_list=component_elements_full)

                    if component_detail is not None:
                        component_detail_new = component_detail
                        component_detail_new['element_background_color'] = element_background_color

                    component_elements_final = []
                    for component in component_elements_full:
                        if component == component_detail:
                            component_elements_final.append(component_detail_new)
                        else:
                            component_elements_final.append(component)

                    updater["component_elements"] = component_elements_final
                
            else:
                return  {"internal_response_code": 1,"message": "failed"}

            homepage_elements_base_update = HomePageElementsBaseUpdateModel(component_elements=updater["component_elements"])
            homepage_elements_model = HomePageElementsUpdateModel(**homepage_elements_base_update.dict())

            result = self.model.update(db=db, db_obj=details, obj_in=homepage_elements_model.dict())
            if result:
                await self.refresh_homepage_redis(db=db, homepage_name=homepage_name)

            return  {"internal_response_code": 0,"message": "success", "data": result} if result else  {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    # async def get_homepage_validations(
    #     self,
    #     user_id: str,
    #     default_title: str,
    #     loc: Optional[CoordinateModel] = None,
    #     title_with_loc_cod: Optional[str] = None,
    # ) -> any:
    #     try:
    #         if title_with_loc_cod != None:
    #             loc_code = title_with_loc_cod.split("_")
    #             if loc_code in LOC_CODES:
    #                 return title_with_loc_cod

    #         if loc != None:
    #             stores_collection = StoresCollection()
    #             serviceable_locations = await stores_collection.get_serviceable_location(coordinates = loc.dict())
    #             if len(serviceable_locations) > 0:
    #                 homepage_title = f'''{default_title}_{serviceable_locations[0]["loc_code"]}'''
    #             else:
    #                 homepage_title = default_title
    #             return homepage_title

    #         # Get primary address
    #         address_collection = AddressCollection()
    #         primary_address = await address_collection.get_primary_address(current_user_id=user_id)
    #         if primary_address != None:
    #             primary_address = primary_address.dict()
    #             current_address_coordinate = CoordinateModel(
    #                 type =  "Point",
    #                 coordinates= primary_address["loc"]
    #             )
    #             stores_collection = StoresCollection()
    #             serviceable_locations = await stores_collection.get_serviceable_location(coordinates = current_address_coordinate.dict())

    #             if len(serviceable_locations) > 0:
    #                 homepage_title = f'''{default_title}_{serviceable_locations[0]["loc_code"]}'''
    #             else:
    #                 homepage_title = default_title
    #             return homepage_title
            
    #         else:
    #             homepage_title = default_title

    #         return homepage_title
    #     except Exception:
    #         raise HTTPException(status_code=500, detail="Something went wrong")
            
    
    async def add_homepage_component_item_list(
        self,
        db: Session,
        code: str,
        add_to_title: str,
        add_to_code: str,
        homepage_name: str,
        component_title: str,
        rank: int
    ) -> any:
        try:
            if homepage_name is None or component_title is None:
                return  {"internal_response_code": 1,"message": "failed"}

            if add_to_title not in VALID_ADD_TO_LIST:
                return  {"internal_response_code": 1,"message": "failed"}

            if homepage_name not in VALID_HOMEPAGE_COMPONENT_NAMES_FOR_PAGES:
                return  {"internal_response_code": 1,"message": "failed"}

            details = await self.get_homepage_by_homepage_name_and_component_title(db=db, code=code, homepage_name=homepage_name, component_title=component_title)

            if details is None:
                return {"internal_response_code": 1,"message": f"""No component with title  -`{component_title}` found"""}

            if add_to_title == "Brand":
                brands_collection = BrandsCollection()
                added = await brands_collection.add_homepage_component_to_brand(db=db, code=add_to_code, rank=rank, homepage_component_data=details.__dict__)
            elif add_to_title == "BrandCollection":
                brands_collections_collection = BrandsCollectionCollection()
                added = await brands_collections_collection.add_homepage_component_to_brand_collection(db=db, code=add_to_code, rank=rank, homepage_component_data=details.__dict__)
            
            else:
                return  {"internal_response_code": 1,"message": "failed"}
            
            
            await self.refresh_homepage_redis(db=db, homepage_name=homepage_name)
            
            return  {"internal_response_code": 0,"message": "success", "data": None}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    

    async def remove_homepage_component_item_list(
        self,
        db: Session,
        code: str,
        add_to_title: str,
        add_to_code: str,
        homepage_name: str,
        component_title: str
    ) -> any:
        try:
            if homepage_name is None or component_title is None:
                return  {"internal_response_code": 1,"message": "failed"}
            
            if add_to_title not in VALID_ADD_TO_LIST:
                return  {"internal_response_code": 1,"message": "failed"}
            
            if homepage_name not in VALID_HOMEPAGE_COMPONENT_NAMES_FOR_PAGES:
                return  {"internal_response_code": 1,"message": "failed"}

            details = await self.get_homepage_by_homepage_name_and_component_title(db=db, code=code, homepage_name=homepage_name, component_title=component_title)

            if details is None:
                return {"internal_response_code": 1,"message": f"""No component with title  -`{component_title}` found"""}

            if add_to_title == "Brand":
                brands_collection = BrandsCollection()
                removed = await brands_collection.remove_homepage_component_from_brand(db=db, code=add_to_code, homepage_component_data=details.__dict__)
            elif add_to_title == "BrandCollection":
                brands_collections_collection = BrandsCollectionCollection()
                removed = await brands_collections_collection.remove_homepage_component_from_brand_collection(db=db, code=add_to_code, homepage_component_data=details.__dict__)
            else:
                return  {"internal_response_code": 1,"message": "failed"}
            
            await self.refresh_homepage_redis(db=db, homepage_name=homepage_name)

            return  {"internal_response_code": 0,"message": "success", "data": removed}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    
    async def refresh_homepage_redis(
        self,
        db: Session,
        homepage_name: str
    ) -> any:
        try:
            await self.redis.delete_list(homepage_name)
            homepage_data = await self.get_homepage_details(homepage_name=homepage_name, db=db, limit=500, page=1, refresh_redis=True)

            for component in homepage_data:
                await self.redis.rpush(homepage_name, component.__dict__)
            
            return True
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def delete_homepage_component(
        self,
        db: Session,
        homepage_code: str,
        homepage_name: str,
    ) -> any:
        try:
            where_clause = f"""code='{homepage_code}' AND homepage_name='{homepage_name}' AND is_deleted=false"""
            existing_homepage_component = self.model.get_one(db=db, where_clause=where_clause, code=homepage_code)
            if existing_homepage_component is None:
                return {"internal_response_code": 1, "message": f"""component with code {homepage_code} and homepage name {homepage_name} not found"""}

            homepage_component_delete_dict = HomePageDeleteModel(code=homepage_code).dict()
            deleted_component = self.model.update(db=db, db_obj=existing_homepage_component, obj_in=homepage_component_delete_dict)

            return {"internal_response_code": 0, "message": f"""homepage component {homepage_code}_{homepage_name} deleted"""} if deleted_component else {"internal_response_code": 1, "message": f"""failed to delete component {homepage_code}_{homepage_name}"""}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Something went wrong")
