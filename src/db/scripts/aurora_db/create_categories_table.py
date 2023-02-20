import aurora_db

def create_categories_table():
    commands = """
        CREATE TABLE categories (
            code TEXT PRIMARY KEY NOT NULL,
            category_name TEXT NOT NULL,
            sort_priority SMALLINT,
            category_logo TEXT,
            category_banner TEXT,
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
    create_categories_table()
