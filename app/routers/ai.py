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
    # 1. Verify document exists & belongs to user
    document=crud.get_document(
        db,
        request.document_id,
        current_user.id
    )

     # 2. Save user's question
    crud.create_chat_message(
    db=db,
    document_id=document.id,
    user_id=current_user.id,
    role="user",
    message=request.question,
)

     # 3. Ask Gemini
    answer = ask_gemini(
    document.extracted_text,
    request.question
)   

      # 4. Save AI's answer
    crud.create_chat_message(
        db=db,
        document_id=document.id,
        user_id=current_user.id,
        role="assistant",
        message=answer,
    )
    

    return schemas.AIResponse(
    answer=answer
)