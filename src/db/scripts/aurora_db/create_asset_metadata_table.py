import aurora_db

def asset_metadata_table():
    commands = """
        CREATE TABLE asset_metadata (
            name TEXT PRIMARY KEY NOT NULL,
            link TEXT NOT NULL,
            dimension TEXT NOT NULL,
            type TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE,
            is_updated BOOLEAN,
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """

    database_function = aurora_db.DatabaseFunction()
    database_function.create_table(commands=commands)
   

if __name__ == '__main__':
    asset_metadata_table()
    
