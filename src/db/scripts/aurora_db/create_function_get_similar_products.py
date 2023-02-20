import aurora_db

def create_get_similar_products():
    commands = """
CREATE or REPLACE FUNCTION get_similar_products(IN brand text, IN product_type text, IN metal text, OUT related_products json, OUT more_from_brand json)
AS 
$$
DECLARE
    limit_product smallint;
BEGIN
    raise notice 'brand: %', $1;
    raise notice 'product_type: %', $2;
	raise notice 'metal: %', $3;
	
	limit_product := 10;
	
	select JSON_AGG((json_build_object ('code',products2.code, 'sku_code',products2.sku_code,'product_tag', products2.product_tag , 'fine_fashion_tag', products2.fine_fashion_tag, 'product_name',products2.product_name,'media', products2.media,'brand', products2.brand,'mrp', products2.mrp, 'discount',products2.discount,'list_price', products2.list_price, 'category1', products2.category1,'product_type1', products2.product_type1))) 
	into more_from_brand from (select 'code',products.code, 'sku_code',products.sku_code,'product_tag', products.product_tag, 'fine_fashion_tag', products.fine_fashion_tag ,'product_name',products.product_name,'media', products.media,'brand', products.brand,'mrp', products.mrp, 'discount',products.discount,'list_price', products.list_price, 'category1', products.category1,'product_type1', products.product_type1  from products join inventory on inventory.sku_code=products.sku_code where products.brand=$1 and live='true' and inventory.qty>0 limit limit_product) products2;
    raise notice 'more_from_brand: %', more_from_brand;

	IF $2 <> '' and $3 <> '' THEN
		select JSON_AGG((json_build_object ('code',products1.code, 'sku_code',products1.sku_code,'product_tag', products1.product_tag, 'fine_fashion_tag', products1.fine_fashion_tag ,'product_name',products1.product_name,'media', products1.media,'brand', products1.brand,'mrp', products1.mrp, 'discount',products1.discount,'list_price', products1.list_price, 'category1', products1.category1,'product_type1', products1.product_type1))) 
		into related_products from (select 'code',products.code, 'sku_code',products.sku_code,'product_tag', products.product_tag, 'fine_fashion_tag', products.fine_fashion_tag ,'product_name',products.product_name,'media', products.media,'brand', products.brand,'mrp', products.mrp, 'discount',products.discount,'list_price', products.list_price, 'category1', products.category1,'product_type1', products.product_type1  from products join inventory on inventory.sku_code=products.sku_code where products.product_type1=$2 and products.metal1=$3 and live='true' and inventory.qty>0 limit limit_product) products1;
		raise notice 'related_products: %', related_products;
	ELSIF $2 <> '' THEN
		select JSON_AGG((json_build_object ('code',products1.code, 'sku_code',products1.sku_code,'product_tag', products1.product_tag, 'fine_fashion_tag', products1.fine_fashion_tag ,'product_name',products1.product_name,'media', products1.media,'brand', products1.brand,'mrp', products1.mrp, 'discount',products1.discount,'list_price', products1.list_price, 'category1', products1.category1,'product_type1', products1.product_type1))) 
		into related_products from (select 'code',products.code, 'sku_code',products.sku_code,'product_tag', products.product_tag, 'fine_fashion_tag', products.fine_fashion_tag ,'product_name',products.product_name,'media', products.media,'brand', products.brand,'mrp', products.mrp, 'discount',products.discount,'list_price', products.list_price, 'category1', products.category1,'product_type1', products.product_type1  from products join inventory on inventory.sku_code=products.sku_code where products.product_type1=$2 and live='true' and inventory.qty>0 limit limit_product) products1;
		raise notice 'related_products: %', related_products;
	ELSIF $3 <> '' THEN
		select JSON_AGG((json_build_object ('code',products1.code, 'sku_code',products1.sku_code,'product_tag', products1.product_tag, 'fine_fashion_tag', products1.fine_fashion_tag ,'product_name',products1.product_name,'media', products1.media,'brand', products1.brand,'mrp', products1.mrp, 'discount',products1.discount,'list_price', products1.list_price, 'category1', products1.category1,'product_type1', products1.product_type1))) 
		into related_products from (select 'code',products.code, 'sku_code',products.sku_code,'product_tag', products.product_tag, 'fine_fashion_tag', products.fine_fashion_tag ,'product_name',products.product_name,'media', products.media,'brand', products.brand,'mrp', products.mrp, 'discount',products.discount,'list_price', products.list_price, 'category1', products.category1,'product_type1', products.product_type1  from products join inventory on inventory.sku_code=products.sku_code where products.metal1=$3 and live='true' and inventory.qty>0 limit limit_product) products1;
		raise notice 'related_products: %', related_products;
	END IF;
	
END $$
LANGUAGE plpgsql;
    """

    database_function = aurora_db.DatabaseFunction()
    database_function.create_function(commands=commands)
   

if __name__ == '__main__':
    create_get_similar_products()