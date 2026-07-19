from sqlalchemy.orm import Session
from app import models, schemas, utils
from sqlalchemy import or_
from fastapi import HTTPException
import os




## DOCUMENTS ##

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


def get_documents(
    db:Session,
):
    return db.query(models.Document).all()




def get_document(db:Session, document_id:int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()



def delete_document(db:Session,document_id:int):
    document =   db.query(models.Document).filter(models.Document.id == document_id).first()     # fetch document metadata
    if not document:                                                              # If document metadata doesnt exists make raise 404 exception
        raise HTTPException(   
        status_code=404,           
        detail="Document not found"
    )
    upload_path = os.path.join("uploads", document.stored_filename)              # Fetch the path
    if os.path.exists(upload_path):                                              # Check document file in path exists
        os.remove(upload_path)                                                   # Remove file

    db.delete(document)                                        # Delete document metadata from database
    db.commit()                                                # Commit changes

    return {"message": "Document deleted successfully"}         # Return message 








## USERS ##

def create_user(db:Session, user: schemas.UserCreate):
    if db.query(models.User).filter(models.User.email==user.email).first():
        raise HTTPException(
            status_code= 409,
            detail="Email already registered"
        )
    hashed_password = utils.hash_password(user.password)
    user = models.User(
       username= user.username,
        email=user.email,
        hashed_password=hashed_password
     )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_identifier(
    db: Session,
    identifier: str
):
    return (
    db.query(models.User)
    .filter(
        or_(
            models.User.email == identifier,
            models.User.username == identifier
        )
    )
    .first()
)