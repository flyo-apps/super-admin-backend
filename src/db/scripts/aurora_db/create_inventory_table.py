import aurora_db

def inventory_table():
    commands = """
        CREATE TABLE inventory (
            sku_code TEXT PRIMARY KEY NOT NULL,
            qty SMALLINT NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """

    database_function = aurora_db.DatabaseFunction()
    database_function.create_table(commands=commands)
   

if __name__ == '__main__':
    inventory_table()
    
