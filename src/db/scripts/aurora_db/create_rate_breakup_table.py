import aurora_db

def create_rate_break_up_table():
    commands = """
        CREATE TABLE rate_breakup (
            code TEXT PRIMARY KEY NOT NULL,
            brand TEXT NOT NULL,
            metal TEXT NOT NULL,
            rate FLOAT NOT NULL,
            weight_type TEXT,
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
    create_rate_break_up_table()
