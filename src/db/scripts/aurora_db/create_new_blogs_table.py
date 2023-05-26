import aurora_db

def create_new_blogs_table():
    commands = """
        CREATE TABLE new_blogs (
            code TEXT PRIMARY KEY NOT NULL,
            screen_filter JSON,
            content TEXT NOT NULL,
            content_summary TEXT NOT NULL,
            rank SMALLINT NOT NULL
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
    create_new_blogs_table()
