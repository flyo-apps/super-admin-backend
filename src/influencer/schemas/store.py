from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, String, DATETIME, Integer, ForeignKey
from items.schemas.products import ProductsSchema

class InfluencerStoreSchema(Base):
    __tablename__ = "influencer_store"

    code = Column(String, primary_key=True, index=True)
    influencer_name = Column(String)
    influencer_handle = Column(String)
    name = Column(String)
    image = Column(String)
    cover_image = Column(String)
    description = Column(String)
    summary = Column(String)
    rank = Column(Integer)
    live = Column(Boolean)
    username = Column(String)
    created_at = Column(DATETIME)
    is_deleted = Column(Boolean)
    deleted_at = Column(DATETIME)