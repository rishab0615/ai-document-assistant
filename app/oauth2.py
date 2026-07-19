from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import SECRET_KEY, ALGORITHM
from app.dependencies import get_db
from app import models


# -------------------------------------------------------------------------
# OAuth2PasswordBearer
#
# This DOES NOT verify the JWT.
#
# Its only job is:
# 1. Look for the "Authorization" header.
# 2. Extract the Bearer token.
# 3. Pass that token to any function that Depends() on it.
#
# Example:
#
# Authorization: Bearer eyJhbGcOiJIUzI1NiIs...
#
# token = "eyJhbGcOiJIUzI1NiIs..."
#
# tokenUrl is mainly used by Swagger UI so it knows users should obtain
# tokens from /auth/login.
# -------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)


# -------------------------------------------------------------------------
# Verify JWT Access Token
#
# Responsibility:
#   Validate that the JWT is genuine and extract the logged-in user's ID.
#
# Input:
#   JWT token
#
# Output:
#   user_id
#
# It DOES NOT query the database.
# It ONLY verifies the token.
# -------------------------------------------------------------------------

def verify_access_token(token: str):

    try:

        # Decode the JWT.
        #
        # This verifies:
        # • Signature (using SECRET_KEY)
        # • Algorithm (HS256)
        # • Expiration time (exp)
        #
        # If anything is invalid, JWTError will be raised.
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Read the "sub" claim.
        #
        # During login we stored:
        #
        # {
        #     "sub": "1"
        # }
        #
        # So this retrieves:
        #
        # user_id = "1"
        user_id = payload.get("sub")

        # If the token does not contain a subject,
        # treat it as invalid.
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )

        # Return the logged-in user's id.
        return user_id

    # Invalid signature
    # Expired token
    # Corrupted token
    # Wrong algorithm
    #
    # All of these end up here.
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )


# -------------------------------------------------------------------------
# Get Current Logged-in User
#
# Responsibility:
#
# JWT
#      ↓
# Verify Token
#      ↓
# Extract User ID
#      ↓
# Query Database
#      ↓
# Return User Object
#
# This is the function that almost every protected endpoint will use.
# -------------------------------------------------------------------------

def get_current_user(

    # FastAPI automatically extracts:
    #
    # Authorization: Bearer <JWT>
    #
    # and passes only the token string here.
    token: str = Depends(oauth2_scheme),

    # FastAPI also creates a database session
    # and injects it here.
    db: Session = Depends(get_db)

):

    # Verify the JWT.
    #
    # If invalid,
    # HTTPException(401) is automatically raised.
    user_id = verify_access_token(token)

    # Fetch the logged-in user from the database.
    current_user = (
        db.query(models.User)
        .filter(models.User.id == int(user_id))
        .first()
    )

    # Imagine:
    #
    # User logs in.
    # JWT is created.
    #
    # Later...
    #
    # Admin deletes that user.
    #
    # JWT is still valid,
    # but the user no longer exists.
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    # Return the complete SQLAlchemy User object.
    #
    # Now anywhere we use:
    #
    # current_user = Depends(get_current_user)
    #
    # we'll have access to:
    #
    # current_user.id
    # current_user.username
    # current_user.email
    #
    return current_user