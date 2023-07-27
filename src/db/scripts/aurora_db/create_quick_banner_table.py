import aurora_db

def create_quick_banners_table():
    commands = """
        CREATE TABLE quick_banners (
            code TEXT PRIMARY KEY NOT NULL,
            screen_filter JSON,
            data JSON[],
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
    create_quick_banners_table()
