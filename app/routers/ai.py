from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud, models, oauth2
from app.dependencies import get_db
from app.services.gemini_service import ask_gemini

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post( "/ask",response_model=schemas.AIResponse)
def ask_question(
    request: schemas.AIQuestion,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    document=crud.get_document(
        db,
        request.document_id,
        current_user.id
    )
    answer = ask_gemini(
    document.extracted_text,
    request.question
)
    return schemas.AIResponse(
    answer=answer
)