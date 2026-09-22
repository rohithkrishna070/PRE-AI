"""
==============================================================================
PRE-AI Auth Controller Router (api/v1/endpoints/auth.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: FastAPI Route Controllers
In FastAPI, route controllers map incoming HTTP REST requests (POST/GET) to 
business service logic and database operations.

Endpoints:
- POST /api/v1/auth/register: Registers a new user.
- POST /api/v1/auth/login: Authenticates user and returns JWT token.
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
    Registers a new user with email, username, and password.
    """
    try:
        user = register_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates user credentials and returns a JWT Access Token.
    """
    user = authenticate_user(db, login_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
