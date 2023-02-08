from db.aurora.aurora_base import Base
from sqlalchemy import Column, ForeignKey, String, ForeignKey, Integer
from items.schemas.products import ProductsSchema

class ProductVariantsMapSchema(Base):
    __tablename__ = "product_variants_map"

    code = Column(String, primary_key=True, index=True)
    unique_id = Column(String, index=True)
    sku_code = Column(String, index=True)

class ProductVariantsSchema(Base):
    __tablename__ = "product_variants"

    code = Column(String, primary_key=True, index=True)
    unique_id = Column(String, ForeignKey(ProductVariantsMapSchema.sku_code))
    variant_name = Column(String)
    variant_type = Column(String)
    sku_code = Column(String, ForeignKey(ProductsSchema.sku_code))
    product_name = Column(String)
    product_image = Column(String)
    rank = Column(Integer)




