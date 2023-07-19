from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, ARRAY, Column, String, DATETIME, JSON, Float


class RateBreakupSchema(Base):
    __tablename__ = "rate_breakup"

    code = Column(String, primary_key=True, index=True)
    brand = Column(String)
    metal = Column(String)
    rate = Column(Float)
    weight_type = Column(String)
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)