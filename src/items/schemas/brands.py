from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, Integer, String, ARRAY, JSON, DATETIME


class BrandsSchema(Base):
    __tablename__ = "brands"

    code = Column(String, primary_key=True, index=True)
    brand_name = Column(String, index=True)
    sort_priority = Column(Integer)
    logo_image = Column(String)
    banner_image = Column(String)
    description = Column(String)
    description_images = Column(ARRAY(String))
    items_list = Column(ARRAY(JSON))
    search_tags = Column(ARRAY(String))
    has_store = Column(Boolean)
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)

