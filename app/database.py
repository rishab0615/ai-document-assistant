from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_URL="postgresql://rishab@localhost/ai_document"

engine =create_engine(DB_URL)

SessionLocal = sessionmaker(
    autocommit = False,
    autoFlush = False,
    bind= engine
)

class Base(DeclarativeBase):
    pass