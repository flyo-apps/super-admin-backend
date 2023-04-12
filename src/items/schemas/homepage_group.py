from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, String, Float, ARRAY, DATETIME


class HomePageCollectionsSchema(Base):
    __tablename__ = "homepage_group"

    code = Column(String, primary_key=True, index=True)
    homepage_collection_name = Column(String, index=True)
    images = Column(ARRAY(String))
    logo_images = Column(ARRAY(String))
    tags = Column(ARRAY(String))
    collection_discount = Column(Float)
    collection_info = Column(String)
    redirect_to = Column(String)
    redirect_type = Column(String)
    redirect_name = Column(String)
    filters = Column(ARRAY(String))
    products = Column(ARRAY(String))
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)
    