from db.aurora.aurora_base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME
from items.schemas.products import ProductsSchema

class InventorySchema(Base):
    __tablename__ = "inventory"

    sku_code = Column(String, ForeignKey(ProductsSchema.sku_code), primary_key=True, index=True)
    qty = Column(Integer)
    updated_at = Column(DATETIME)

