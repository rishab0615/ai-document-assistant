from fastapi import APIRouter, Depends, UploadFile, File  # Split endpoints using APi router into files ex documents ,auth etc
from sqlalchemy.orm import Session
from app import crud,schemas
from app.dependencies import get_db
import os
import uuid

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/")
def upload_document(
    title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    extension = os.path.splitext(file.filename)[1]
    stored_filename = f"{uuid.uuid4()}{extension}"

    upload_path = os.path.join("uploads", stored_filename)

    with open(upload_path, "wb") as buffer:
        buffer.write(file.file.read())
     
    db_doc =  crud.create_doc(
      db = db, 
      document=schemas.DocumentCreate(
      title = title,
      original_filename = file.filename,
      stored_filename =   stored_filename   ,
      content_type =    file.content_type,      
      file_size =      file.size     
         )

    )
    
    return db_doc


