from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ARRAY, DATETIME
from .products import ProductsSchema


class ProductCollectionSchema(Base):
    __tablename__ = "product_collection"

    code = Column(String, primary_key=True, index=True)
    collection_name = Column(String, index=True)
    collection_details = Column(String)
    search_tags = Column(ARRAY(String))
    collection_images  = Column(ARRAY(String))
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)


class ProductCollectionItemsSchema(Base):
    __tablename__ = "product_collection_items"

    code = Column(String, primary_key=True, index=True)
    collection_name = Column(String, index=True)
    collection_code = Column(String, index=True)
    sort_priority = Column(Integer)
    sku_code = Column(Integer, ForeignKey(ProductsSchema.sku_code))