"""
==============================================================================
PRE-AI Auth Controller Router (api/v1/endpoints/auth.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: FastAPI Route Controllers
In FastAPI, route controllers map incoming HTTP REST requests (POST/GET) to 
business service logic and database operations.

Syntax Breakdown:
- `@router.post(...)`: Maps an HTTP POST endpoint.
- `status_code=status.HTTP_201_CREATED`: Sets 201 Created header on successful signup.
- `response_model=UserResponse`: Ensures passwords are never returned in JSON responses.
- `HTTPException`: Generates RFC-compliant JSON error bodies.
==============================================================================
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services.auth_service import register_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Functionality:
    Registers a new user with email, username, and password.

    Syntax:
    - `user_in: UserCreate`: Request body validated against Pydantic schema.
    - `status.HTTP_201_CREATED`: Standard HTTP response code for resource creation.
    """
    try:
        user = register_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    """
    Functionality:
    Authenticates user credentials and returns a signed JWT Access Token.

    Syntax:
    - `status.HTTP_401_UNAUTHORIZED`: Returns 401 code if credentials do not match.
    - `headers={"WWW-Authenticate": "Bearer"}`: Standard OAuth2/JWT challenge header.
    """
    user = authenticate_user(db, login_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Syntax: Issues a signed JWT with user ID as subject ('sub')
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
