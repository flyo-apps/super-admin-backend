import aurora_db

def create_stories_table():
    commands = """
        CREATE TABLE stories (
            code TEXT PRIMARY KEY NOT NULL,
            story_name TEXT NOT NULL,
            story_logo TEXT NOT NULL,
            story_image TEXT,
            description TEXT,
            redirection_type TEXT,
            redirection_text TEXT,
            redirection_value TEXT,
            filters JSON,
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
    create_stories_table()