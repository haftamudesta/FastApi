from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(
    settings.DATABASE_URL
)

sessionLocal = sessionmaker(autocomplete=False, autoflush=False, bind=engine)
base = declarative_base()


def get_db():
    db = sessionLocal
    try:
        yield db
    finally:
        db.close()


def create_tables():
    base.metadata.create_all(bind=engine)
