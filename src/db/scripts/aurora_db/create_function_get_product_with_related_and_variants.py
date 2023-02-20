import aurora_db

def create_get_product_with_related_and_variants():
    commands = """
CREATE or REPLACE FUNCTION get_product_with_related_and_variants(IN sku_code text, OUT product_data json, OUT product_variants_data json, OUT reviews_data json)
AS
$$
DECLARE
    product_variants_map_data text[];
BEGIN
    select row_to_json(final_row) INTO product_data from  (select products.*,inventory.qty from products left join inventory on products.sku_code=inventory.sku_code where products.sku_code=$1) as final_row;
    raise notice 'Value: %', product_data;
	select json_agg(five_reviws) into reviews_data from (select product_reviews from product_reviews where product_reviews.sku_code=$1 order by product_reviews.rating  limit 5) five_reviws; 
    if product_data IS NOT NULL THEN
        select array_agg(unique_id::TEXT) INTO product_variants_map_data from product_variants_map where product_variants_map.sku_code=$1;
        raise notice 'Value two: %', product_variants_map_data;
    end if;
            
    if product_variants_map_data IS NOT NULL THEN
        select JSON_AGG(json_build_object('product_variants',product_variants,
            'product',json_build_object('code',products.code,'sku_code',products.sku_code, 'sku_code',products.sku_code, 'media',products.media, 'mrp',products.mrp, 'list_price',products.list_price, 'discount',products.discount, 'category1', products.category1,'product_type1', products.product_type1, 'brand', products.brand)))
            INTO product_variants_data from product_variants join products on
            product_variants.sku_code=products.sku_code and product_variants.unique_id = ANY (product_variants_map_data) order by product_variants_data ->> '$.product_variants.rank';
        raise notice 'Value three: %', product_variants_data;
    end if;
END $$
LANGUAGE plpgsql;
    """

    database_function = aurora_db.DatabaseFunction()
    database_function.create_function(commands=commands)
   

if __name__ == '__main__':
    create_get_product_with_related_and_variants()


# CREATE or REPLACE FUNCTION get_product_with_related_and_variants(IN sku_code text, OUT product_data json,OUT all_product_variants json)
# -- RETURNS json[]
# AS
# $$
# DECLARE
# -- 	product_data json;
#     product_variants_map_data text[];
#     product_variants_data text[];
# -- 	return_obj json[]
# -- 	all_product_variants json[];
# BEGIN
#     select row_to_json(products)::JSON INTO product_data from products where products.sku_code=$1;
# 	raise notice 'Value: %', product_data;
# 	if product_data IS NOT NULL THEN
# 		select array_agg(unique_id::TEXT) INTO product_variants_map_data from product_variants_map where product_variants_map.sku_code=$1;
# 		raise notice 'Value two: %', product_variants_map_data;
# 	end if;
            
# 	if product_variants_map_data IS NOT NULL THEN
# 		select array_agg(product_variants.sku_code) INTO product_variants_data from product_variants where product_variants.unique_id = ANY (product_variants_map_data);
# 		raise notice 'Value three: %', product_variants_data;
# 	end if;
	
# 	if product_variants_data IS NOT NULL THEN
# 		select JSON_AGG(products)::JSON INTO all_product_variants from products where products.sku_code = ANY (product_variants_data);
# 		raise notice 'Value four: %', all_product_variants;
# 	end if;
# -- 	return_obj := array
# -- 	select * into return_val from json_to_record('{"product":product_data,"product_variants": all_product_variants}') as x(product json, product_variants json[]);
# -- 	return return_val;
# END $$
# LANGUAGE plpgsql;