from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, String, DATETIME, JSON

class StoriesSchema(Base):
    __tablename__ = "stories"

    code = Column(String, primary_key=True, index=True)
    story_name = Column(String, index=True)
    story_logo = Column(String)
    story_image = Column(String)
    description = Column(String)
    redirection_type = Column(String)
    redirection_text = Column(String)
    redirection_value = Column(String)
    filters = Column(JSON)
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)