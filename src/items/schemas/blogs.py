from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, ARRAY, Column, String, DATETIME, JSON, Integer


class BlogsSchema(Base):
    __tablename__ = "blogs"

    code = Column(String, primary_key=True, index=True)
    blog_code = Column(String)
    blog_name = Column(String)
    blog_rank = Column(Integer)
    blog_summary_image = Column(String)
    blog_type = Column(String)
    text = Column(String)
    image = Column(String)
    element_type = Column(String)
    element_code = Column(String)
    filter = Column(JSON)
    width_percentage = Column(String)
    dimension = Column(String)
    rank = Column(Integer)
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)

class NewBlogsSchema(Base):
    __tablename__ = "new_blogs"

    code = Column(String, primary_key=True, index=True)
    screen_filter = Column(JSON)
    content = Column(String)
    content_summary = Column(String)
    rank = Column(Integer)
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)
