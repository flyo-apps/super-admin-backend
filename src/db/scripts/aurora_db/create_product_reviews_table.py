import aurora_db

def create_product_reviews_table():
    commands = """
        CREATE TABLE product_reviews (
            code TEXT PRIMARY KEY NOT NULL,
            sku_code TEXT NOT NULL,
            title TEXT,
            review TEXT NOT NULL,
            rating FLOAT NOT NULL,
            customer_name TEXT NOT NULL,
            created_at DATE,
            is_updated BOOLEAN,
            updated_at TIMESTAMP WITH TIME ZONE,
            is_deleted BOOLEAN,
            deleted_at TIMESTAMP WITH TIME ZONE
        )
    """
    database_function = aurora_db.DatabaseFunction()
    database_function.create_table(commands=commands)
   

if __name__ == '__main__':
    create_product_reviews_table()