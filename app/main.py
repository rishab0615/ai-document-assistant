# IMPORTS
from fastapi import FastAPI
from app.database import engine, Base
from app import models            # This is imported but not used becuase
                                  # it executes and lets Base know these models exits

from app.routers import documents
from app.routers import auth



# FASTAPI APP
app=FastAPI()


# CREATE NON EXISTING Tables
Base.metadata.create_all(bind=engine)


# Routes
app.include_router(documents.router)
app.include_router(auth.router)


