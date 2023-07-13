import aurora_db

def create_multi_stories_table():
    commands = """
        CREATE TABLE multi_stories (
            code TEXT PRIMARY KEY NOT NULL,
            story_name TEXT NOT NULL,
            story_logo TEXT NOT NULL,
            description TEXT,
            stories JSON[],
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
    create_multi_stories_table()