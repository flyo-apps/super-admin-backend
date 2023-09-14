import aurora_db

def create_blog_for_listing_page_table():
    commands = """
        CREATE TABLE blog_for_listing_page (
            code TEXT PRIMARY KEY NOT NULL,
            image TEXT NOT NULL,
            rank SMALLINT NOT NULL,
            screen_filter JSON NOT NULL,
            blog_code TEXT NOT NULL,
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
    create_blog_for_listing_page_table()
