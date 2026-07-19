from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import schemas, crud

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):        
    return crud.create_user(db,user)

