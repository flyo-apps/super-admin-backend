from db.aurora.aurora_base import Base
from sqlalchemy import Boolean, Column, String, DATETIME
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import deferred
from sqlalchemy.types import TypeDecorator
import base64

class JSONCompatibleBytea(TypeDecorator):
    impl = BYTEA

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return base64.b64encode(value).decode()

    @staticmethod
    def coerce_compared_value(op, value):
        if isinstance(value, str):
            return base64.b64decode(value.encode())
        return value

class AssetMetadataSchema(Base):
    __tablename__ = "asset_metadata"

    name = Column(String, primary_key=True, index=True)
    link = Column(String)
    dimension = Column(String)
    type = Column(String)
    blob_filedata = Column(BYTEA)
    created_at = Column(DATETIME)
    is_updated = Column(Boolean)
    updated_at = Column(DATETIME)
