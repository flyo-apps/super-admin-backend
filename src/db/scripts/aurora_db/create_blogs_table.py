import aurora_db

def create_blogs_table():
    commands = """
        CREATE TABLE blogs (
            code TEXT PRIMARY KEY NOT NULL,
            blog_code TEXT NOT NULL,
            blog_name TEXT NOT NULL,
            blog_rank SMALLINT,
            blog_summary_image TEXT NOT NULL,
            blog_type TEXT NOT NULL,
            text TEXT,
            image TEXT,
            element_type TEXT NOT NULL,
            element_code TEXT,
            filter JSON,
            width_percentage FLOAT,
            dimension TEXT,
            rank SMALLINT,
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
    create_blogs_table()
