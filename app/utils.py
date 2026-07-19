from passlib.context import CryptContext
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from sqlalchemy import DateTime


pwd_context = CryptContext(                  # This is used to perform hashing operations
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):            
    return pwd_context.hash(password)           # Return hashed


def verify_password(plain_password: str, hashed_password: str):    
    return pwd_context.verify(plain_password,hashed_password)                 # Return true or false



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt    


    