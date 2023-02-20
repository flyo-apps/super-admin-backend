import aurora_db

def create_product_variants_table():
    commands = """
        CREATE TABLE product_variants (
            code TEXT PRIMARY KEY NOT NULL,
            unique_id TEXT NOT NULL,
            variant_name TEXT NOT NULL,
            variant_type TEXT NOT NULL,
            sku_code TEXT NOT NULL,
            product_name TEXT NOT NULL,
            product_image TEXT NOT NULL,
            rank smallint
        )
    """

    database_function = aurora_db.DatabaseFunction()
    database_function.create_table(commands=commands)

def create_product_variants_map_table():
    commands = """
        CREATE TABLE product_variants_map (
            code TEXT PRIMARY KEY NOT NULL,
            unique_id TEXT NOT NULL,
            sku_code TEXT NOT NULL
        )
    """

    database_function = aurora_db.DatabaseFunction()
    database_function.create_table(commands=commands)


if __name__ == '__main__':
    create_product_variants_table()
    create_product_variants_map_table()
