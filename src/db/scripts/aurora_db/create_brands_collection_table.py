import aurora_db

def create_collections_table():
    commands = """
        CREATE TABLE brands_collection (
            code TEXT PRIMARY KEY NOT NULL,
            brand_collection_name TEXT NOT NULL,
            sort_priority SMALLINT,
            brand_name TEXT,
            collection_logo TEXT,
            collection_banner TEXT,
            description TEXT,
            description_images TEXT[],
            items_list JSON[],
            search_tags TEXT[],
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
    create_collections_table()
