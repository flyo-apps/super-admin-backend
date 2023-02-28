from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, Integer, String, ARRAY, JSON, DATETIME

class HomepageSchema(Base):
    __tablename__ = "homepage"

    code = Column(String, primary_key=True, index=True)
    homepage_name = Column(String, index=True)
    component_title = Column(String, index=True)
    title_tag = Column(String)
    description_tag = Column(String)
    h1_tag = Column(String)
    component_type = Column(String)
    component_elements_type = Column(String)
    component_elements = Column(ARRAY(JSON))
    component_rank = Column(Integer)
    component_secondary_title = Column(String)
    widget_redirect_to = Column(String)
    show_title = Column(Boolean)
    max_visible_element = Column(Integer)
    component_category_link = Column(String)
    component_background_color = Column(String)
    type = Column(String)
    ui_specs  = Column(JSON)
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)