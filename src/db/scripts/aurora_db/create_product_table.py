import aurora_db

def create_product_table():
    commands = """
        CREATE TABLE products (
            code TEXT PRIMARY KEY NOT NULL,
            sku_code TEXT NOT NULL,
            product_name TEXT NOT NULL,
            brand TEXT NOT NULL,
            brand_code TEXT,
            upc TEXT,
            hsn TEXT NOT NULL,
            category1 TEXT NOT NULL,
            category2 TEXT,
            category3 TEXT,
            usecase1 TEXT NOT NULL,
            usecase2 TEXT,
            usecase3 TEXT,
            usecase4 TEXT,
            usecase5 TEXT,
            product_type1 TEXT NOT NULL,
            product_type2 TEXT,
            product_type3 TEXT,
            style_code TEXT,
            collection TEXT,
            vendor TEXT,
            vendor_sku_code TEXT,
            gender TEXT NOT NULL,
            size TEXT,
            size_unit TEXT,
            metal1 TEXT,
            metal2 TEXT,
            metal3 TEXT,
            material1 TEXT,
            material2 TEXT,
            material3 TEXT,
            stone1 TEXT,
            stone2 TEXT,
            stone3 TEXT,
            colour1 TEXT,
            colour2 TEXT,
            colour3 TEXT,
            metal_colour1 TEXT,
            metal_colour2 TEXT,
            metal_colour3 TEXT,
            style_of_jewellery TEXT,
            plating TEXT,
            warranty TEXT,
            gst_percent SMALLINT,
            shipping_time TEXT,
            purity TEXT,
            designer TEXT,
            gifting BOOLEAN,
            virtual_try_on BOOLEAN,
            description TEXT,
            description_images TEXT[],
            care_instruction TEXT,
            disclaimer TEXT,
            year SMALLINT,
            season TEXT,
            certificate_type TEXT,
            product_tag TEXT,
            fine_fashion_tag TEXT,
            search_tags TEXT[],
            weight FLOAT,
            weight_unit TEXT,
            seller_panel TEXT,
            mrp FLOAT NOT NULL,
            msp FLOAT,
            list_price FLOAT NOT NULL,
            media JSON[],
            pdp_strip_images JSON[],
            viewing_or_bought TEXT,
            returnable BOOLEAN,
            returnable_policy TEXT,
            replaceable BOOLEAN,
            replaceable_policy TEXT,
            only_prepaid BOOLEAN,
            seo_title TEXT,
            seo_description TEXT,
            seo_canonical_url TEXT,
            seo_tags TEXT,
            seo_keywords TEXT[],
            items_list JSON[],
            is_bestseller BOOLEAN,
            google_product_category TEXT,
            age_group TEXT,
            mpn TEXT,
            adwords_grouping TEXT,
            adwords_label TEXT,
            condition TEXT,
            custom_product TEXT,
            custom_label TEXT[],
            live BOOLEAN,
            country_of_origin TEXT,
            discount FLOAT, 
            created_at TIMESTAMP WITH TIME ZONE,
            is_updated BOOLEAN,
            updated_at TIMESTAMP WITH TIME ZONE,
            is_deleted BOOLEAN,
            deleted_at TIMESTAMP WITH TIME ZONE,
            sort_priority1 SMALLINT,
            sort_priority2 SMALLINT,
            sort_priority3 SMALLINT,
            sort_priority4 SMALLINT,
            sort_priority5 SMALLINT,
            products_list JSON[],
            manufacturer_name TEXT,
            manufacturer_address TEXT,
            manufacturer_pincode TEXT,
            is_customizable BOOLEAN,
            production_strategy TEXT,
            vendor_code TEXT,
            pickup_city TEXT,
            finish_and_design TEXT,
            brand_description_images TEXT[],
            brand_offer_strip JSON[],
            style_note TEXT,
            design_type TEXT,
            express_shipping BOOLEAN,
            collection2 TEXT,
            collection3 TEXT,
            collection4 TEXT,
            pick_pack_time SMALLINT,
            title_tag TEXT,
            description_tag TEXT,
            h1_tag TEXT,
            certificate_image TEXT,
            product_details JSON,
            price_breakup JSON
        )
    """

    database_function = aurora_db.DatabaseFunction()
    database_function.create_table(commands=commands)

if __name__ == '__main__':
    create_product_table()
