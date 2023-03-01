import aurora_db

def create_brand_table():
    commands = """
        CREATE TABLE brands (
            code TEXT PRIMARY KEY NOT NULL,
            brand_name TEXT NOT NULL,
            sort_priority SMALLINT NOT NULL,
            logo_image TEXT,
            banner_image TEXT,
            description TEXT,
            description_images TEXT[],
            items_list JSON[],
            search_tags TEXT[],
            has_store BOOLEAN,
            created_at TIMESTAMP WITH TIME ZONE,
            is_updated BOOLEAN,
            updated_at TIMESTAMP WITH TIME ZONE,
            is_deleted BOOLEAN,
            deleted_at TIMESTAMP WITH TIME ZONE
        )
    """
    
    database_function = aurora_db.DatabaseFunction()
    database_function.create_table(commands=commands)
   

if __name__ == '__main__':
    create_brand_table()
    
