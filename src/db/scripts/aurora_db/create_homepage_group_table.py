import aurora_db

def create_homepage_group_table():
    commands = """
        CREATE TABLE homepage_group (
            code TEXT PRIMARY KEY NOT NULL,
            homepage_collection_name TEXT NOT NULL,
            images TEXT[],
            logo_images TEXT[],
            tags TEXT[],
            collection_discount FLOAT,
            collection_info TEXT,
            redirect_to TEXT,
            redirect_type TEXT,
            redirect_name TEXT,
            filters TEXT[],
            products TEXT[],
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
    create_homepage_group_table()
