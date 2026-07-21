from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, oauth2, schemas
from app.dependencies import get_db
from app.services.gemini_service import (
    ask_gemini,
    build_chat_history,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/ask", response_model=schemas.AIResponse)
def ask_question(
    request: schemas.AIQuestion,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    # 1. Verify document exists and belongs to current user
    document = crud.get_document(
        db=db,
        document_id=request.document_id,
        user_id=current_user.id,
    )

    # 2. Save user's question
    crud.create_chat_message(
        db=db,
        document_id=document.id,
        user_id=current_user.id,
        role="user",
        message=request.question,
    )

    # 3. Load previous conversation
    messages = crud.get_chat_history(
        db=db,
        document_id=document.id,
        user_id=current_user.id,
    )
   # Remove the current question that was just saved
    messages = messages[:-1]
    # 4. Keep only the latest conversation
    messages = messages[-6:]

    # 5. Convert conversation into prompt text
    chat_history = build_chat_history(messages)

    # 6. Ask Gemini
    answer = ask_gemini(
        document_text=document.extracted_text,
        chat_history=chat_history,
        question=request.question,
    )

    # 7. Save assistant reply
    crud.create_chat_message(
        db=db,
        document_id=document.id,
        user_id=current_user.id,
        role="assistant",
        message=answer,
    )

    # 8. Return response
    return schemas.AIResponse(
        answer=answer,
    )