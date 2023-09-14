from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, String, Integer, DATETIME, DATE, JSON

class BlogsForListingPageSchema(Base):
    __tablename__ = "blog_for_listing_page"

    code = Column(String, primary_key=True, index=True)
    image = Column(String)
    rank = Column(Integer)
    screen_filter = Column(JSON)
    blog_code = Column(String)
    created_at = Column(DATE)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)