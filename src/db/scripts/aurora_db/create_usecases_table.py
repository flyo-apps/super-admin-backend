import aurora_db

def create_usecases_table():
    commands = """
        CREATE TABLE usecases (
            code TEXT PRIMARY KEY NOT NULL,
            usecase_name TEXT NOT NULL,
            sort_priority SMALLINT,
            usecase_logo TEXT,
            usecase_banner TEXT,
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
    create_usecases_table()
