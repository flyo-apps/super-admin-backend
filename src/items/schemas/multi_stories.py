from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, String, DATETIME, JSON, ARRAY

class MultiStoriesSchema(Base):
    __tablename__ = "multi_stories"

    code = Column(String, primary_key=True, index=True)
    story_name = Column(String, index=True)
    story_logo = Column(String)
    description = Column(String)
    stories = Column(ARRAY(JSON))
    chip_data = Column(ARRAY(JSON))
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)