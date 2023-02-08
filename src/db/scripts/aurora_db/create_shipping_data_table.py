import aurora_db

def create_shipping_data_table():
    commands = """
        CREATE TABLE shipping_data (
            code TEXT PRIMARY KEY NOT NULL,
            seller_warehouse TEXT NOT NULL,
            drop_city TEXT NOT NULL,
            drop_pincode TEXT NOT NULL,
            drop_state TEXT,
            tat SMALLINT NOT NULL,
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
    create_shipping_data_table()
    
