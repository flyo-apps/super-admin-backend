from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, String, Float, DATETIME, DATE

class ProductReviewSchema(Base):
    __tablename__ = "product_reviews"

    code = Column(String, primary_key=True, index=True)
    sku_code = Column(String)
    title = Column(String)
    review = Column(String)
    rating = Column(Float)
    customer_name = Column(String)
    created_at = Column(DATE)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)