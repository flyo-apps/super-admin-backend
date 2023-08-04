from fastapi import HTTPException
from items.utils.constants import SORTING_LIST, FILTER_MAP

async def get_product_filters_where_clause(
    filters_dict: dict
) -> any:
    try:
        where_clause = ""

        if not bool(filters_dict):
            where_clause = where_clause + " (live=true) AND"
            where_clause = where_clause + " (is_deleted=false) AND"
            where_clause = where_clause + " (sort_priority1 > 0)"
            return where_clause

        if "category" in filters_dict and filters_dict["category"]  != None and len(filters_dict["category"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["category"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(category1) IN ({array_val}) OR lower(category2) IN ({array_val}) OR lower(category3) IN ({array_val}) ) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "gender" in filters_dict and filters_dict["gender"]  != None and len(filters_dict["gender"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["gender"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" (lower(gender) IN ({array_val})  )"""
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "product_type" in filters_dict and filters_dict["product_type"]  != None and len(filters_dict["product_type"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["product_type"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(product_type1) IN ({array_val}) OR lower(product_type2) IN ({array_val}) OR lower(product_type3) IN ({array_val}) ) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "occasion" in filters_dict and filters_dict["occasion"]  != None and len(filters_dict["occasion"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["occasion"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(usecase1) IN ({array_val}) OR lower(usecase2) IN ({array_val}) OR lower(usecase3) IN ({array_val}) OR lower(usecase4) IN ({array_val}) OR lower(usecase5) IN ({array_val})) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "collection" in filters_dict and filters_dict["collection"]  != None and len(filters_dict["collection"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["collection"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(collection) IN ({array_val}) OR lower(collection2) IN ({array_val}) OR lower(collection3) IN ({array_val}) OR lower(collection4) IN ({array_val})) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "brand" in filters_dict and filters_dict["brand"]  != None and len(filters_dict["brand"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["brand"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(brand) IN ({array_val}) ) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "design_type" in filters_dict and filters_dict["design_type"]  != None and len(filters_dict["design_type"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["design_type"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(design_type) IN ({array_val}) ) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "size" in filters_dict and filters_dict["size"]  != None and len(filters_dict["size"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["size"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(size) IN ({array_val}) ) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "discount" in filters_dict and filters_dict["discount"]  != None and len(filters_dict["discount"])>0:
            values = await get_discount_min_max(filters_dict["discount"])
            min_val = values[0]/100
            max_val = values[1]/100
            query_string_local = f""" (discount BETWEEN {min_val} AND {max_val} ) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "price" in filters_dict and filters_dict["price"]  != None and len(filters_dict["price"])>0:
            query_string_local = query_string_local = f""" (list_price BETWEEN {filters_dict["price"][0]} AND {filters_dict["price"][1]})"""
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "metal" in filters_dict and filters_dict["metal"]  != None and len(filters_dict["metal"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["metal"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(metal1) IN ({array_val}) OR lower(metal2) IN ({array_val}) or lower(metal3) IN ({array_val}) ) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "material" in filters_dict and filters_dict["material"]  != None and len(filters_dict["material"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["material"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(material1) IN ({array_val}) OR lower(material2) IN ({array_val}) or lower(material3) IN ({array_val}) ) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "stone" in filters_dict and filters_dict["stone"]  != None and len(filters_dict["stone"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["stone"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(stone1) IN ({array_val}) OR lower(stone2) IN ({array_val}) or lower(stone3) IN ({array_val}))"""
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "colour" in filters_dict and filters_dict["colour"]  != None and len(filters_dict["colour"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["colour"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(colour1) IN ({array_val}) OR lower(colour2) IN ({array_val}) or lower(colour3) IN  ({array_val})) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "metal_colour" in filters_dict and filters_dict["metal_colour"]  != None and len(filters_dict["metal_colour"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["metal_colour"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(metal_colour1) IN ({array_val}) OR lower(metal_colour2) IN ({array_val}) or lower(metal_colour3) IN ({array_val})) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "style_of_jewellery" in filters_dict and filters_dict["style_of_jewellery"]  != None and len(filters_dict["style_of_jewellery"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["style_of_jewellery"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(style_of_jewellery) IN ({array_val})) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "plating" in filters_dict and filters_dict["plating"]  != None and len(filters_dict["plating"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["plating"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(plating) IN ({array_val})) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "warranty" in filters_dict and filters_dict["warranty"]  != None and len(filters_dict["warranty"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["warranty"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(warranty) IN ({array_val})) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "shipping_time" in filters_dict and filters_dict["shipping_time"]  != None and len(filters_dict["shipping_time"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["shipping_time"]]
            array_val = ','.join(filter_values)
            # array_val = ', '.join(map(str, filters_dict["shipping_time"]))
            query_string_local = f""" ( lower(shipping_time) IN ({array_val})) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "purity" in filters_dict and filters_dict["purity"]  != None and len(filters_dict["purity"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["purity"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(purity) IN ({array_val})) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "designer" in filters_dict and filters_dict["designer"]  != None and len(filters_dict["designer"])>0:
            filter_values = ["'" + filter_val.lower() + "'" for filter_val in filters_dict["designer"]]
            array_val = ','.join(filter_values)
            query_string_local = f""" ( lower(designer) IN ({array_val})) """
            if(where_clause != ""):
                where_clause = where_clause + "AND"
            where_clause = where_clause + query_string_local
        if "gifting" in filters_dict and filters_dict["gifting"]  != None and len(filters_dict["gifting"])>0:
            if len(filters_dict["gifting"]) == 1:
                query_string_local = f""" (gifting={filters_dict["gifting"][0]}) """
                if(where_clause != ""):
                    where_clause = where_clause + "AND"
                where_clause = where_clause + query_string_local
        if "virtual_try_on" in filters_dict and filters_dict["virtual_try_on"]  != None and len(filters_dict["virtual_try_on"])>0:
            if len(filters_dict["virtual_try_on"]) == 1:
                query_string_local = f""" (virtual_try_on={filters_dict["virtual_try_on"][0]}) """
                if(where_clause != ""):
                    where_clause = where_clause + "AND"
                where_clause = where_clause + query_string_local
            
        if(where_clause != ""):
            where_clause = where_clause + "AND"
        where_clause = where_clause + " (live=true) AND"
        where_clause = where_clause + " (is_deleted=false) AND"
        where_clause = where_clause + " (sort_priority1 > 0)"

        return where_clause
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

async def get_product_filters_where_clause_for_elastic(
    filters_dict: dict
) -> any:
    try:
        filter_array = []
        if not bool(filters_dict):
            live_product = {"match": { "live": "true"}}
            is_deleted_product = {"match": { "is_deleted": "false"}}
            sort_priority1_product = { "range": { "sort_priority1": { "gt": 0 }}}
            inventory_product = { "range": { "qty": { "gt": 0 }}}
            filter_array.append(live_product)
            filter_array.append(is_deleted_product)
            filter_array.append(sort_priority1_product)
            filter_array.append(inventory_product)
            return filter_array
        
        if "category" in filters_dict and filters_dict["category"]  != None and len(filters_dict["category"])>0:
            category1_filter = {"terms": { "category1":filters_dict["category"]}}
            category2_filter = {"terms": { "category2":filters_dict["category"]}}
            category3_filter = {"terms": { "category3":filters_dict["category"]}}
            category_filter_array = []
            category_filter_array.append(category1_filter) 
            category_filter_array.append(category2_filter) 
            category_filter_array.append(category3_filter) 
            category_filter_object = {
                "bool":{
                    "should": category_filter_array
                }
            }
            filter_array.append(category_filter_object)
        
        if "gender" in filters_dict and filters_dict["gender"]  != None and len(filters_dict["gender"])>0:
            design_type_filter = {"terms": { "gender": filters_dict["gender"]}}
            filter_array.append(design_type_filter)


        if "product_type" in filters_dict and filters_dict["product_type"]  != None and len(filters_dict["product_type"])>0:
            product_type1_filter = {"terms": { "product_type1": filters_dict["product_type"]}}
            product_type2_filter = {"terms": { "product_type2": filters_dict["product_type"]}}
            product_type3_filter = {"terms": { "product_type3":filters_dict["product_type"]}}
            product_type_filter_array = []
            product_type_filter_array.append(product_type1_filter)
            product_type_filter_array.append(product_type2_filter)
            product_type_filter_array.append(product_type3_filter)

            product_type_filter_object = {
                "bool":{
                    "should": product_type_filter_array
                }
            }
            filter_array.append(product_type_filter_object)

        if "occasion" in filters_dict and filters_dict["occasion"]  != None and len(filters_dict["occasion"])>0:
            usecase1_filter = {"terms": { "usecase1": filters_dict["occasion"]}}
            usecase2_filter = {"terms": { "usecase2": filters_dict["occasion"]}}
            usecase3_filter = {"terms": { "usecase3": filters_dict["occasion"]}}
            usecase4_filter = {"terms": { "usecase4": filters_dict["occasion"]}}
            usecase5_filter = {"terms": { "usecase5": filters_dict["occasion"]}}
            usecase_filter_array = []
            usecase_filter_array.append(usecase1_filter)
            usecase_filter_array.append(usecase2_filter)
            usecase_filter_array.append(usecase3_filter)
            usecase_filter_array.append(usecase4_filter)
            usecase_filter_array.append(usecase5_filter)

            usecase_filter_object = {
                "bool":{
                    "should": usecase_filter_array
                }
            }
            filter_array.append(usecase_filter_object)

        if "collection" in filters_dict and filters_dict["collection"]  != None and len(filters_dict["collection"])>0:
            collection_filter = {"terms": { "collection": filters_dict["collection"]}}
            collection2_filter = {"terms": { "collection2": filters_dict["collection"]}}
            collection3_filter = {"terms": { "collection3": filters_dict["collection"]}}
            collection4_filter = {"terms": { "collection4": filters_dict["collection"]}}
            collection_filter_array = []
            collection_filter_array.append(collection_filter)
            collection_filter_array.append(collection2_filter)
            collection_filter_array.append(collection3_filter)
            collection_filter_array.append(collection4_filter)

            collection_filter_object = {
                "bool":{
                    "should": collection_filter_array
                }
            }
            filter_array.append(collection_filter_object)


        if "brand" in filters_dict and filters_dict["brand"]  != None and len(filters_dict["brand"])>0:
            brand_filter = {"terms": { "brand": filters_dict["brand"]}}
            filter_array.append(brand_filter)

        if "design_type" in filters_dict and filters_dict["design_type"]  != None and len(filters_dict["design_type"])>0:
            design_type_filter = {"terms": { "design_type": filters_dict["design_type"]}}
            filter_array.append(design_type_filter)

        if "size" in filters_dict and filters_dict["size"]  != None and len(filters_dict["size"])>0:
            size_filter = {"terms": { "size": filters_dict["size"]}}
            filter_array.append(size_filter)

        if "discount" in filters_dict and filters_dict["discount"]  != None and len(filters_dict["discount"])>0:
            values = await get_discount_min_max(filters_dict["discount"])
            min_val = values[0]/100
            max_val = values[1]/100

            discount_filter = { "range": { "discount": { "gte": min_val,  "lte": max_val} } }
            filter_array.append(discount_filter)

        if "price" in filters_dict and filters_dict["price"]  != None and len(filters_dict["price"])>0:
            price_filter = { "range": { "list_price": { "gte": filters_dict["price"][0],  "lte": filters_dict["price"][1]} } }
            filter_array.append(price_filter)

        if "metal" in filters_dict and filters_dict["metal"]  != None and len(filters_dict["metal"])>0:
            metal1_filter = {"terms": { "metal1": filters_dict["metal"]}}
            metal2_filter = {"terms": { "metal2": filters_dict["metal"]}}
            metal3_filter = {"terms": { "metal3": filters_dict["metal"]}}
            metal_filter_array = []
            metal_filter_array.append(metal1_filter)
            metal_filter_array.append(metal2_filter)
            metal_filter_array.append(metal3_filter)

            metal_filter_object = {
                "bool":{
                    "should": metal_filter_array
                }
            }
            filter_array.append(metal_filter_object)

        if "material" in filters_dict and filters_dict["material"]  != None and len(filters_dict["material"])>0:
            material1_filter = {"terms": { "material1": filters_dict["material"]}}
            material2_filter = {"terms": { "material2": filters_dict["material"]}}
            material3_filter = {"terms": { "material3": filters_dict["material"]}}
            material_filter_array = []
            material_filter_array.append(material1_filter)
            material_filter_array.append(material2_filter)
            material_filter_array.append(material3_filter)

            material_filter_object = {
                "bool":{
                    "should": material_filter_array
                }
            }
            filter_array.append(material_filter_object)

        # if "stone" in filters_dict and filters_dict["stone"]  != None and len(filters_dict["stone"])>0:
        #     filter_values = ["'" + filter_val + "'" for filter_val in filters_dict["stone"]]
        #     array_val = ','.join(filter_values)
        #     query_string_local = f""" (stone1 IN ({array_val}) OR stone2 IN ({array_val}) or stone3 IN ({array_val}))"""
        #     if(where_clause != ""):
        #         where_clause = where_clause + "AND"
        #     where_clause = where_clause + query_string_local

        if "colour" in filters_dict and filters_dict["colour"]  != None and len(filters_dict["colour"])>0:
            colour1_filter = {"terms": { "colour1": filters_dict["colour"]}}
            colour2_filter = {"terms": { "colour2": filters_dict["colour"]}}
            colour3_filter = {"terms": { "colour3": filters_dict["colour"]}}
            colour_filter_array = []
            colour_filter_array.append(colour1_filter)
            colour_filter_array.append(colour2_filter)
            colour_filter_array.append(colour3_filter)

            colour_filter_object = {
                "bool":{
                    "should": colour_filter_array
                }
            }
            filter_array.append(colour_filter_object)

        if "metal_colour" in filters_dict and filters_dict["metal_colour"]  != None and len(filters_dict["metal_colour"])>0:
            metal1_colour_filter = {"terms": { "metal_colour1": filters_dict["metal_colour"]}}
            metal2_colour_filter = {"terms": { "metal_colour2": filters_dict["metal_colour"]}}
            metal3_colour_filter = {"terms": { "metal_colour3": filters_dict["metal_colour"]}}
            metal_colour_filter_array = []
            metal_colour_filter_array.append(metal1_colour_filter)
            metal_colour_filter_array.append(metal2_colour_filter)
            metal_colour_filter_array.append(metal3_colour_filter)

            metal_colour_filter_object = {
                "bool":{
                    "should": metal_colour_filter_array
                }
            }
            filter_array.append(metal_colour_filter_object)


        # if "style_of_jewellery" in filters_dict and filters_dict["style_of_jewellery"]  != None and len(filters_dict["style_of_jewellery"])>0:
        #     filter_values = ["'" + filter_val + "'" for filter_val in filters_dict["style_of_jewellery"]]
        #     array_val = ','.join(filter_values)
        #     query_string_local = f""" (style_of_jewellery IN ({array_val})) """
        #     if(where_clause != ""):
        #         where_clause = where_clause + "AND"
        #     where_clause = where_clause + query_string_local

        if "plating" in filters_dict and filters_dict["plating"]  != None and len(filters_dict["plating"])>0:
            plating_filter = {"terms": { "plating": filters_dict["plating"]}}
            filter_array.append(plating_filter)

        if "warranty" in filters_dict and filters_dict["warranty"]  != None and len(filters_dict["warranty"])>0:
            warranty_filter = {"terms": { "warranty": filters_dict["warranty"]}}
            filter_array.append(warranty_filter)

        if "shipping_time" in filters_dict and filters_dict["shipping_time"]  != None and len(filters_dict["shipping_time"])>0:
            shipping_time_filter = {"terms": { "shipping_time": filters_dict["shipping_time"]}}
            filter_array.append(shipping_time_filter)

        if "purity" in filters_dict and filters_dict["purity"]  != None and len(filters_dict["purity"])>0:
            purity_filter = {"terms": { "purity": filters_dict["purity"]}}
            filter_array.append(purity_filter)

        if "gifting" in filters_dict and filters_dict["gifting"]  != None and len(filters_dict["gifting"])>0:
            gifting_filter = {"terms": { "gifting": filters_dict["gifting"]}}
            filter_array.append(gifting_filter)

        # if "virtual_try_on" in filters_dict and filters_dict["virtual_try_on"]  != None and len(filters_dict["virtual_try_on"])>0:
        #     if len(filters_dict["virtual_try_on"]) == 1:
        #         query_string_local = f""" (virtual_try_on={filters_dict["virtual_try_on"][0]}) """
        #         if(where_clause != ""):
        #             where_clause = where_clause + "AND"
        #         where_clause = where_clause + query_string_local

        live_product = {"match": { "live": "true"}}
        is_deleted_product = {"match": { "is_deleted": "false"}}
        sort_priority1_product = { "range": { "sort_priority1": { "gt": 0 }}}
        inventory_product = { "range": { "qty": { "gt": 0 }}}
        filter_array.append(live_product)
        filter_array.append(is_deleted_product)
        filter_array.append(sort_priority1_product)
        filter_array.append(inventory_product)
        return filter_array

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


async def get_product_sorting_clause(
    sorting_method: str,
) -> any:
    try:
        if sorting_method == None:
            return "sort_priority1 DESC, sort_priority2 DESC, sort_priority3 DESC, sort_priority4 DESC, sort_priority5 DESC, product_name"
        elif sorting_method.lower() == "What's New".lower():
            return "created_at DESC, sort_priority1 DESC, product_name"
        elif sorting_method.lower() == "Price - Low to High".lower():
            return "list_price ASC, sort_priority1 DESC, product_name"
        elif sorting_method.lower() == "Price - High to Low".lower():
            return "list_price DESC, sort_priority1 DESC, product_name"
        elif sorting_method.lower() == "Popularity".lower():
            return "sort_priority1 DESC, sort_priority2 DESC, sort_priority3 DESC, sort_priority4 DESC, sort_priority5 DESC, product_name"
        elif sorting_method.lower() == "Discount - Low to High".lower():
            return "discount ASC, sort_priority1 DESC, product_name"
        elif sorting_method.lower() == "Discount - High to Low".lower():
            return "discount DESC, sort_priority1 DESC, product_name"
        elif sorting_method not in SORTING_LIST:
            return "sort_priority1 DESC, sort_priority2 DESC, sort_priority3 DESC, sort_priority4 DESC, sort_priority5 DESC, product_name"
        else:
            return "sort_priority1 DESC, sort_priority2 DESC, sort_priority3 DESC, sort_priority4 DESC, sort_priority5 DESC, product_name"

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


async def get_product_sorting_clause_for_elastic(
    sorting_method: str,
) -> any:
    try:
        if sorting_method == None or sorting_method not in SORTING_LIST or sorting_method == "Popularity":
            return [{
                "_score": "desc",
                "sort_priority1": "desc",
                "sort_priority2": "desc",
                "sort_priority3": "desc",
                "sort_priority4": "desc",
                "sort_priority5": "desc",
                "sku_code": "desc"
            }]
        elif sorting_method == "What's New":
            return [{
                "created_at": "desc",
                "sku_code": "desc"
            }]
        elif sorting_method == "Price - Low to High":
            return [{
                "list_price": "asc",
                "sku_code": "asc"
            }]
        elif sorting_method == "Price - High to Low":
            return [{
                "list_price": "desc",
                "sku_code": "desc"
            }]
        elif sorting_method == "Discount - Low to High":
            return [{
                "discount": "asc",
                "sku_code": "asc"
            }]
        elif sorting_method == "Discount - High to Low":
            return [{
                "discount": "desc",
                "sku_code": "desc"
            }]
        else:
            return [{
                "_score": "desc",
                "sort_priority1": "desc",
                "sort_priority2": "desc",
                "sort_priority3": "desc",
                "sort_priority4": "desc",
                "sort_priority5": "desc",
                "sku_code": "desc"
            }]

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


async def get_product_filter_group_by_and_select_clause(
    current_selection: str,
) -> any:
    try:
        return FILTER_MAP[f"""{current_selection}"""]["group_by"], FILTER_MAP[f"""{current_selection}"""]["select_statement"], FILTER_MAP[f"""{current_selection}"""]["order_by"]
    except Exception as e:
        print(e, "get_product_filter_group_by_and_select_clause")
        raise HTTPException(status_code=500, details="Something went wrong")

async def get_discount_min_max(
    selected_filter: list
) -> any:
    try:
        if len(selected_filter) == 1:
            if selected_filter[0] == f"""10% and above""":
                return [10, 100]
            elif selected_filter[0] == f"""20% and above""":
                return [20, 100]
            elif selected_filter[0] == f"""30% and above""":
                return [30, 100]
            elif selected_filter[0] == f"""40% and above""":
                return [40, 100]
            elif selected_filter[0] == f"""50% and above""":
                return [50, 100]
            elif selected_filter[0] == f"""60% and above""":
                return [60, 100]
            elif selected_filter[0] == f"""70% and above""":
                return [70, 100]
            else:
                return [0, 100]
        elif len(selected_filter) == 2 and selected_filter[0].isnumeric() and selected_filter[0].isnumeric():
            return [int(selected_filter[0]), int(selected_filter[1])]
        else:
            return await get_min_max_of_discount(selected_filter)
        
    except Exception:
        raise HTTPException(status_code=500, details="Something went wrong")


async def get_min_max_of_discount(selected_filter: list) -> any:
    try:
        val1 = []
        for val in selected_filter:
            if val == f"""10% and above""":
                val1.append(10)
            elif val == f"""20% and above""":
                val1.append(20)
            elif val == f"""30% and above""":
                val1.append(30)
            elif val == f"""40% and above""":
                val1.append(40)
            elif val == f"""50% and above""":
                val1.append(50)
            elif val == f"""60% and above""":
                val1.append(60)
            elif val == f"""70% and above""":
                val1.append(70)
        
        if len(val1) > 0:
            return [min(val1), 100]
        
        return [0, 100]
    except Exception:
        raise HTTPException(status_code=500, details="Something went wrong")