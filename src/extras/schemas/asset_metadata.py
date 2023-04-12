from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, String, DATETIME

class AssetMetadataSchema(Base):
    __tablename__ = "asset_metadata"

    name = Column(String, primary_key=True, index=True)
    link = Column(String)
    dimension = Column(String)
    type = Column(String)
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
