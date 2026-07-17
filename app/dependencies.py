from app.database import SessionLocal


def get_db():
    db = SessionLocal()          # This creates a new database session

    try:
        yield db                 # This gives session to the router toia.  return db

    finally:                     # The should always close even if there is an exception
        db.close()     