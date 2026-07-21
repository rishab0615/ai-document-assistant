from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import DB_URL

DB_URL=DB_URL

engine =create_engine(DB_URL)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind= engine
)

class Base(DeclarativeBase):
    pass