from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "postgresql://"+os.environ.get("AURORA_USER")+":"+os.environ.get("AURORA_PASSWORD")+"@"+os.environ.get("AURORA_URL")+"/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)