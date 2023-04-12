from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, ARRAY, JSON, DATETIME
from sqlalchemy.orm import relationship


class UsecasesSchema(Base):
    __tablename__ = "usecases"

    code = Column(String, primary_key=True, index=True)
    usecase_name = Column(String, index=True)
    sort_priority = Column(Integer)
    usecase_logo = Column(String)
    usecase_banner = Column(String)
    description = Column(String)
    description_images =  Column(ARRAY(String))
    items_list = Column(ARRAY(JSON))
    search_tags =  Column(ARRAY(String))
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)