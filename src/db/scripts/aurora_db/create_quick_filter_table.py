import aurora_db

def create_quick_filters_table():
    commands = """
        CREATE TABLE quick_filters (
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
    create_quick_filters_table()
