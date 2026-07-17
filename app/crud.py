from sqlalchemy.orm import Session
from app import models, schemas

def create_doc(
    db:Session, 
    document: schemas.DocumentCreate
    ):
    db_doc = models.Document(
        title=document.title,
        original_filename = document.original_filename,
        stored_filename = document.stored_filename,
        content_type = document.content_type,
        file_size = document.file_size                        
)

    db.add(db_doc)                                             # Stage object for insertion
    db.commit()                                                # Save changes to database
    db.refresh(db_doc)                                         # Reload object from database (db.query(Model)  # Read data)
    return db_doc 
