from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, Integer, String, DATETIME


class ShippingDataSchema(Base):
    __tablename__ = "shipping_data"

    code = Column(String, primary_key=True, index=True)
    seller_warehouse = Column(String)
    drop_city = Column(String)
    drop_pincode = Column(String)
    drop_state = Column(String)
    tat = Column(Integer)
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)