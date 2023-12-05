from typing import Generator
from sqlalchemy.orm import declarative_base, sessionmaker
from app.api.core.config import get_settings
from sqlalchemy import create_engine

settings = get_settings()
Base = declarative_base()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db_dependency()->Generator:
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

