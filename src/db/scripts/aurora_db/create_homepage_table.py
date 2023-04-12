import aurora_db

def create_homepage_table():
    commands = """
        CREATE TABLE homepage (
            code TEXT PRIMARY KEY NOT NULL,
            homepage_name TEXT NOT NULL,
            component_title TEXT NOT NULL,
            title_tag TEXT NOT NULL,
            description_tag TEXT NOT NULL,
            h1_tag TEXT NOT NULL,
            component_type TEXT NOT NULL,
            component_elements_type TEXT,
            component_elements JSON[],
            component_rank SMALLINT,
            show_title BOOLEAN,
            max_visible_element SMALLINT,
            component_secondary_title TEXT,
            widget_redirect_to TEXT,
            component_category_link TEXT,
            component_background_color TEXT,
            type TEXT,
            ui_specs JSON,
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
    create_homepage_table()
    
