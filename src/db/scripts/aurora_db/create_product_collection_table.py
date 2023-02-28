import aurora_db

def product_collection_table():
    commands = """
        CREATE TABLE product_collection (
            code TEXT PRIMARY KEY NOT NULL,
            collection_name TEXT NOT NULL,
            collection_details TEXT,
            search_tags TEXT[],
            collection_images TEXT[],
            created_at TIMESTAMP WITH TIME ZONE,
            is_updated BOOLEAN,
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """

    database_function = aurora_db.DatabaseFunction()
    database_function.create_table(commands=commands)
   

if __name__ == '__main__':
    product_collection_table()
    
