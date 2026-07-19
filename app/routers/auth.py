from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import schemas, crud, utils

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):        
    return crud.create_user(db,user)


@router.post("/login",response_model=schemas.Token)
def login_user(user:schemas.UserLogin,db:Session=Depends(get_db)):
    user_db=crud.get_user_by_identifier(db,user.identifier)
    if not user_db:
        raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )
    if not utils.verify_password(
        user.password,
        user_db.hashed_password
    ):
        raise HTTPException(
        status_code= 401,
        detail="Invalid credentials"
    )
    access_token = utils.create_access_token(
    {
        "sub": str(user_db.id)
    }
)
    return {
    "access_token": access_token,
    "token_type": "bearer"
    }
 