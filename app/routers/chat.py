from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud, models, oauth2
from app.dependencies import get_db

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get(
    "/{document_id}",
    response_model=list[schemas.ChatMessageResponse]
)
def get_chat_history(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return crud.get_chat_history(
        db=db,
        document_id=document_id,
        user_id=current_user.id
    )


@router.delete("/{document_id}")
def delete_chat_history(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return crud.delete_chat_history(
        db=db,
        document_id=document_id,
        user_id=current_user.id
    )