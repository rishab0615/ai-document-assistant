from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException

from app import models, schemas, utils

import os


# ==========================================================
# DOCUMENTS
# ==========================================================

def create_doc(
    db: Session,
    document: schemas.DocumentCreate,
    user_id: int,
    extracted_text: str
):
    """
    Create a new document and assign ownership
    to the currently logged-in user.
    """

    db_doc = models.Document(
        user_id=user_id,
        extracted_text=extracted_text,
        original_filename=document.original_filename,
        stored_filename=document.stored_filename,
        content_type=document.content_type,
        file_size=document.file_size
    )

    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    return db_doc


def get_documents(
    db: Session,
    user_id: int
):
    """
    Return ONLY documents belonging
    to the current user.
    """

    return (
        db.query(models.Document)
        .filter(models.Document.user_id == user_id)
        .all()
    )


def get_document(
    db: Session,
    document_id: int,
    user_id: int
):
    """
    Return a single document ONLY if
    it belongs to the logged-in user.
    """

    document = (
        db.query(models.Document)
        .filter(
            models.Document.id == document_id,
            models.Document.user_id == user_id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document


def delete_document(
    db: Session,
    document_id: int,
    user_id: int
):
    """
    Delete a document ONLY if
    it belongs to the logged-in user.
    """

    document = (
        db.query(models.Document)
        .filter(
            models.Document.id == document_id,
            models.Document.user_id == user_id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    upload_path = os.path.join(
        "uploads",
        document.stored_filename
    )

    if os.path.exists(upload_path):
        os.remove(upload_path)

    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully"
    }


# ==========================================================
# USERS
# ==========================================================

def create_user(
    db: Session,
    user: schemas.UserCreate
):
    """
    Register a new user.
    """

    if (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    ):
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    if (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    ):
        raise HTTPException(
            status_code=409,
            detail="Username already taken"
        )

    hashed_password = utils.hash_password(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_identifier(
    db: Session,
    identifier: str
):
    """
    Find a user using either
    email or username.
    """

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


# ==========================================================
# CHATS
# ==========================================================

def create_chat_message(
    db: Session,
    document_id: int,
    user_id: int,
    role: str,
    message: str,
) -> models.ChatMessage:

    chat_message = models.ChatMessage(
        document_id=document_id,
        user_id=user_id,
        role=role,
        message=message,
    )

    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)

    return chat_message

def get_chat_history(
    db: Session,
    document_id: int,
    user_id: int,
):
    return (
        db.query(models.ChatMessage)
        .filter(
            models.ChatMessage.document_id == document_id,
            models.ChatMessage.user_id == user_id,
        )
        .order_by(models.ChatMessage.created_at.asc())
        .all()
    )    



def delete_document(
    db,
    document_id: int,
    user_id: int,
):
    document = (
        db.query(models.Document)
        .filter(
            models.Document.id == document_id,
            models.Document.user_id == user_id,
        )
        .first()
    )

    if document is None:
        return None

    # Delete chat history
    db.query(models.ChatMessage).filter(
        models.ChatMessage.document_id == document.id
    ).delete()

    # Delete PDF from disk
    if document.stored_filename:
        file_path = os.path.join(
            "uploads",
            document.stored_filename,
        )

        if os.path.exists(file_path):
            os.remove(file_path)

    # Delete document
    db.delete(document)
    db.commit()

    return True