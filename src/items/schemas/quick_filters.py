from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, ARRAY, Column, String, DATETIME, JSON, Integer


class QuickFiltersSchema(Base):
    __tablename__ = "quick_filters"

    code = Column(String, primary_key=True, index=True)
    screen_filter = Column(JSON)
    data = Column(ARRAY(JSON))
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)