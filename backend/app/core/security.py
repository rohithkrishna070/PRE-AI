"""
==============================================================================
PRE-AI Security & Cryptography Module (core/security.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Security is essential for any web platform. This module handles 2 main tasks:

1. Password Hashing (Bcrypt):
   - Passwords must NEVER be stored in plain text in a database.
   - We use `passlib` with `bcrypt` to hash passwords before storing them.
   - Hashing is a one-way mathematical function. Even if a hacker steals the DB, 
     they cannot reverse the hash back into the plain text password.

2. JSON Web Tokens (JWT):
   - When a user logs in, the server signs a digital token (JWT) containing 
     their user ID and expiration time.
   - The user's browser sends this token in the header of every future API request:
     `Authorization: Bearer <token>`
   - The server verifies the cryptographic signature to identify the user statelessly.
==============================================================================
"""

from datetime import datetime, timedelta
from typing import Any, Union
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# ------------------------------------------------------------------------------
# 1. CryptContext Setup for Password Hashing
# ------------------------------------------------------------------------------
# CryptContext defines the algorithm configuration. We use 'bcrypt' as default.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------------------------------------------------------------
# 2. Password Hashing Helper Functions
# ------------------------------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a user-entered plain text password against the hashed password stored in the DB.
    Returns True if they match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Takes a plain text password and returns its secure Bcrypt hash digest.
    Example: 'mysecret123' -> '$2b$12$e8a...hashedstring'
    """
    return pwd_context.hash(password)


# ------------------------------------------------------------------------------
# 3. JWT Token Generation Helper Function
# ------------------------------------------------------------------------------
def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    Generates a signed JWT Access Token for authentication.
    
    Parameters:
    - subject: Usually the user's ID or Email address.
    - expires_delta: Optional custom token lifetime. Defaults to settings expiration.
    
    Returns:
    - Encoded JWT string.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Payload contains claims (token payload dictionary)
    to_encode = {
        "exp": expire,             # Expiration Timestamp
        "sub": str(subject),       # Subject (User ID)
        "iat": datetime.utcnow()   # Issued At Timestamp
    }
    
    # Cryptographically sign payload using server's SECRET_KEY and ALGORITHM
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt
