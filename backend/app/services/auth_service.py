"""
==============================================================================
PRE-AI Authentication Service (services/auth_service.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Handles user registration, authentication credential checking, and JWT token issuance.
==============================================================================
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token


def register_user(db: Session, user_in: UserCreate) -> User:
    """
    Registers a new user in the database after hashing their password.
    """
    # Check if user email already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise ValueError("User with this email already exists")

    # Hash the password
    hashed_pwd = get_password_hash(user_in.password)

    # Create new User ORM instance
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_pwd,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, login_in: UserLogin) -> Optional[User]:
    """
    Authenticates a user by email and password.
    Returns User instance if valid, None if invalid.
    """
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user:
        return None
    if not verify_password(login_in.password, user.hashed_password):
        return None
    return user
