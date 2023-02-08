from typing import List, Optional, Union
from datetime import datetime
from fastapi import HTTPException
from ..utils.random_number import (
    get_random_rating
)
from ..models.products import (
    ProductDeleteModel,
    ProductUpdateDescriptionModel,
    ProductUpdateSeoModel,
    ProductUpdateStateModel,
    ProductCreateBaseModel,
    ProductUpdateBaseModel,
    ProductCreateModel,
    ProductUpdateModel,
    ProductUpdateDescriptionBaseModel,
    ProductUpdateSeoBaseModel,
    ProductUpdateStateBaseModel,
)
from ..schemas.products import (
    ProductsSchema
)
from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session

class ProductsCollection:
    def __init__(self):
        self.model = CRUDBase(ProductsSchema)

    async def create_product(
        self,
        products_details: ProductCreateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""(sku_code='{products_details.sku_code}')"""
            existing_product = self.model.get_one(db=db, where_clause=where_clause)
            if existing_product is not None:
                return {"internal_response_code": 1, "message": f"""product with sku_code {products_details.sku_code} exists"""}

            product_create = ProductCreateModel(**products_details.dict())
            created_product = self.model.create(db=db, obj_in=product_create)

            return created_product if created_product else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def upsert_multiple_products(
        self,
        products_details: List[Union[ProductCreateBaseModel,ProductUpdateBaseModel]],
        db: Session
    ) -> any:
        try:
            codes = ','.join(["'" + data.code + "'" for data in products_details])
            existing_codes = []
            where_clause = f"""code IN ({codes})"""
            existing_products = self.model.get_all(db=db, where_clause=where_clause,skip=0,limit=len(products_details))
            if existing_products:
                existing_codes = [data.code for data in existing_products]

            create_products_dict_list = []
            update_products_dict_list = []
            for product in products_details:
                if product.code not in existing_codes:
                    create_product = ProductCreateModel(**product.dict())
                    create_products_dict_list.append(create_product.dict())
                else:
                    product_update = ProductUpdateModel(**product.dict(exclude_unset=True))
                    update_products_dict_list.append(product_update.dict(exclude_none=True))

            res = self.model.bulk_upsert(db=db, update_vals=update_products_dict_list,insert_vals=create_products_dict_list)
            return {"internal_response_code": 0, "message": f"""products created for {len(create_products_dict_list)} codes and updated for {len(update_products_dict_list)} codes"""} if res is None else {"internal_response_code": 1, "message": f"""upsert operation failed"""}
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def update_product(
        self,
        product_update_details: ProductUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""((code='{product_update_details.code}') AND (sku_code='{product_update_details.sku_code}'))"""
            product = self.model.get_one(db=db, where_clause=where_clause)
            if product == None:
                return {"internal_response_code": 1, "sku_code": product_update_details.sku_code, "message": "Product not found"}

            product_update = ProductUpdateModel(**product_update_details.dict(exclude_unset=True))
            product_update.is_updated = True
            product_update.updated_at = datetime.now()
            
            updated_product = self.model.update(db=db, db_obj=product,obj_in=product_update)

            return {"internal_response_code": 0, "sku_code": product_update_details.sku_code, "message": "Product updated"} if updated_product else {"internal_response_code": 1, "sku_code": product_update_details.sku_code, "message": "Product not updated"}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def bulk_update_products(
        self,
        product_update_details: List[ProductUpdateBaseModel],
        db: Session
    ) -> any:
        try:
            update_products_dict_list = []

            for product in product_update_details:
                product_update = ProductUpdateModel(
                    **product.dict(exclude_unset=True))
                product_update.is_updated = True
                product_update.updated_at = datetime.now()

                update_products_dict_list.append(product_update.dict(exclude_none=True))

            result = self.model.bulk_update(db=db, update_vals=update_products_dict_list)

            return {"internal_response_code": 0, "message": "Products updated"} if result is None else {"internal_response_code": 1, "message": "Products not updated"}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_product_state(
        self,
        product_update_state_details: ProductUpdateStateBaseModel,
        db: Session
    ) -> any:
        try: 
            where_clause = f"""((code='{product_update_state_details.code}') AND (sku_code='{product_update_state_details.sku_code}'))"""
            product = self.model.get_one(db=db, where_clause=where_clause)
            if product == None:
                return {"internal_response_code": 1, "sku_code": product_update_state_details.sku_code, "message": "Product not found"}

            product_update = ProductUpdateStateModel(**product_update_state_details.dict(exclude_unset=True))
            product_update.is_updated = True
            product_update.updated_at = datetime.now()
            
            if product == None:
                return {"internal_response_code": 1, "sku_code": product_update.sku_code, "message": "Product not found"}
            updated_product = self.model.update(db=db, db_obj=product,obj_in=product_update)

            return {"internal_response_code": 0, "sku_code": product_update.sku_code, "message": "Product State updated"} if updated_product else {"internal_response_code": 1, "sku_code":  product_update.sku_code, "message": "Product State not updated"}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def bulk_update_products_state(
        self,
        products_update_state_details: List[ProductUpdateStateBaseModel],
        db: Session
    ) -> any:
        try:
            update_products_state_dict_list = []

            for product_state in products_update_state_details:
                product_update = ProductUpdateStateModel(**product_state.dict(exclude_unset=True))
                product_update.is_updated = True
                product_update.updated_at = datetime.now()
                update_products_state_dict_list.append(
                    product_update.dict(exclude_none=True))

            updated_product = self.model.bulk_update(db=db, update_vals=update_products_state_dict_list)

            return {"internal_response_code": 0, "message": f"""product state updated for {len(update_products_state_dict_list)} products"""} if updated_product is None else {"internal_response_code": 1, "message": "failed to update product state"}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_product_desc(
        self,
        product_update_description_details: ProductUpdateDescriptionBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""((code='{product_update_description_details.code}') AND (sku_code='{product_update_description_details.sku_code}'))"""
            product = self.model.get_one(db=db, where_clause=where_clause)
            if product == None:
                return {"internal_response_code": 1, "sku_code": product_update_description_details.sku_code, "message": "Product not found"}

            product_update = ProductUpdateDescriptionModel(**product_update_description_details.dict(exclude_unset=True))
            product_update.is_updated = True
            product_update.updated_at = datetime.now()
            if product == None:
                return {"internal_response_code": 1, "sku_code": product_update.sku_code, "message": "Product not found"}
            updated_product = self.model.update(db=db, db_obj=product,obj_in=product_update)

            return {"internal_response_code": 0, "sku_code":  product_update.sku_code, "message": "Product Description updated"} if updated_product else {"internal_response_code": 1, "sku_code":  product_update.sku_code, "message": "Product Description not updated"}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def bulk_update_products_desc(
        self,
        products_update_description_details: ProductUpdateDescriptionBaseModel,
        db: Session
    ) -> any:
        try:
            update_products_description_list = []

            for product_state in products_update_description_details:
                product_update = ProductUpdateDescriptionModel(
                    **product_state.dict(exclude_unset=True))
                product_update.is_updated = True
                product_update.updated_at = datetime.now()
                update_products_description_list.append(
                    product_update.dict(exclude_none=True))

            updated_product = self.model.bulk_update(
                db=db, update_vals=update_products_description_list)

            return {"internal_response_code": 0, "message": f"""product description updated for {len(update_products_description_list)} products"""} if updated_product is None else {"internal_response_code": 1, "message": "failed to update product description"}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_product_seo(
        self,
        product_update_seo_details: ProductUpdateSeoBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""((code='{product_update_seo_details.code}') AND (sku_code='{product_update_seo_details.sku_code}'))"""
            product = self.model.get_one(db=db, where_clause=where_clause)
            if product == None:
                return {"internal_response_code": 1, "sku_code": product_update_seo_details.sku_code, "message": "Product not found"}

            product_update = ProductUpdateSeoModel(**product_update_seo_details.dict(exclude_unset=True))
            product_update.is_updated = True
            product_update.updated_at = datetime.now()
            if product == None:
                return {"internal_response_code": 1, "sku_code": product_update.sku_code, "message": "Product not found"}
            updated_product = self.model.update(db=db, db_obj=product,obj_in=product_update)

            return {"internal_response_code": 0, "sku_code":  product_update.sku_code, "message": "Product SEO updated"} if updated_product else {"internal_response_code": 1, "sku_code":  product_update.sku_code, "message": "Product SEO not updated"}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_product_by_sku_code(
        self,
        sku_code: str,
        db: Session,
        products_mapping: Optional[bool] = False
    ) -> any:
        try:
            where_clause = f"""(sku_code='{sku_code}' AND live=true AND is_deleted=false)"""
            if products_mapping == False:
                product = self.model.get_one(db=db, where_clause=where_clause)
                return {"internal_response_code": 0, "message": "Success", "data":product} if product else {"internal_response_code": 1, "message": "Failed", "data": None}
           
            query = f"""select * from get_product_with_related_and_variants('{sku_code}')"""
            products = self.model.call_postgres_function(db=db, query=query)
            products_final_data = {}
            if products[0][0] == None:
                return {"internal_response_code": 1, "message": "Failed", "data": None}
        
            products_final_data["product"] = products[0][0]
            rating = await get_random_rating()
            if rating == None:
                rating = 4.8
            
            products_final_data["product"]["rating"] = rating

            brand = products_final_data["product"]["brand"]
            if brand == None:
                brand =  ''
            product_type = products_final_data["product"]["product_type1"]
            if product_type == None:
                product_type =  '' 
            metal = products_final_data["product"]["metal1"]
            if metal == None:
                metal =  ''

            query_similar_products = f"""select * from get_similar_products('{brand}', '{product_type}', '{metal}')"""
            similar_products = self.model.call_postgres_function(db=db, query=query_similar_products)
            
            products_final_data["similar_products"] = []

            if similar_products[0][1] != None and len(similar_products[0][1]) > 0:
                more_from_the_brand = {
                    "pdp_title" : f"""More by {brand}""",
                    "title": f"""{brand}""",
                    "products" : similar_products[0][1],
                    "filter": { "brand": [f"""{brand}"""]} if brand != '' else []
                }
                products_final_data["similar_products"].append(more_from_the_brand)

            if similar_products[0][0] != None and len(similar_products[0][0]) > 0:
                related_product = {
                    "pdp_title": f"""Similar Products""",
                    "title": f"""{metal} {product_type}""",
                    "products": similar_products[0][0],
                    "filter": { 
                        "product_type": [f"""{product_type}"""] if product_type != '' else [],
                        "metal": [f"""{metal}"""] if metal != '' else [] 
                    }
                }
                products_final_data["similar_products"].append(related_product)


            product_reviews_array = products[0][2]

            product_reviews_array_final = []
            if product_reviews_array != None:
                for product_review in product_reviews_array:
                    product_reviews_array_final.append(product_review["product_reviews"])
            
            products_final_data["product_reviews"] = product_reviews_array_final

            if products[0][1] == None:
                return {"internal_response_code": 10, "message": "Success", "data": products_final_data}

            products_final_data["product_variants"] = {}

            for value in products[0][1]:
                unique_id = value["product_variants"]["unique_id"]
                if not f"""{unique_id}""" in products_final_data["product_variants"].keys():
                    products_final_data["product_variants"][f"""{unique_id}"""] = {
                        "variant": {
                            "code": value["product_variants"]["code"],
                            "unique_id": value["product_variants"]["unique_id"],
                            "variant_name": value["product_variants"]["variant_name"],
                            "variant_type": value["product_variants"]["variant_type"],
                        }
                    }
                    products_final_data["product_variants"][f"""{unique_id}"""]["products"] = {
                        f"""{value["product"]["sku_code"]}""": {
                            **value["product"],
                            "product_name": value["product_variants"]["product_name"],
                            "product_image": value["product_variants"]["product_image"],
                            "rank": value["product_variants"]["rank"]
                        }
                    }

                else:
                    products_final_data["product_variants"][f"""{unique_id}"""]["products"][f"""{value["product"]["sku_code"]}"""] = {
                        **value["product"],
                        "product_name": value["product_variants"]["product_name"],
                        "product_image": value["product_variants"]["product_image"],
                        "rank": value["product_variants"]["rank"]
                    }
            
            products_final_data["product_variants"] = list(products_final_data["product_variants"].values())

            all_variants = products_final_data["product_variants"][0]["products"]
            sort_products_in_variants = dict(sorted(all_variants.items(), key=lambda x: x[1]["rank"]), reverse=True)
            del sort_products_in_variants["reverse"]
            products_final_data["product_variants"][0]["products"] = sort_products_in_variants
            
            
            return {"internal_response_code": 10, "message": "Success", "data": products_final_data} if products else {"internal_response_code": 1, "message": "Failed", "data": None}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def delete_product(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            product_delete = ProductDeleteModel(code=code)
            product_delete_dict = product_delete.dict()
            product = self.model.get_one(db=db, code=code)
            if product == None:
                {"internal_response_code": 1, "code": code, "message": "Product not found"}
            deleted_product = self.model.update(db=db, db_obj=product,obj_in=product_delete_dict)

            return {"internal_response_code": 0, "code": code, "message": "Product deleted"} if deleted_product else {"internal_response_code": 1, "code": code, "message": "Product not deleted"} 
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_products_by_sku_codes(
        self,
        db: Session,
        sku_codes: List[str]
    ) -> any:
        try:
            if len(sku_codes) <= 0:
                return None
            
            sku_codes_values = ["'" + name + "'" for name in sku_codes]
            array_val = ','.join(sku_codes_values)
            where_clause = f"""sku_code IN ({array_val})"""

            products_list = self.model.get_all(db=db, where_clause=where_clause)
            return products_list
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")