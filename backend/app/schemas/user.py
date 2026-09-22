"""
==============================================================================
PRE-AI User Pydantic Schemas (schemas/user.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Why do we need Pydantic Schemas if we already have SQLAlchemy Models?
- SQLAlchemy Models represent SQL Database Tables (how data is stored in DB).
- Pydantic Schemas validate HTTP Request & Response Data (how data enters/exits API).

Example:
- When a user signs up, the request contains a plain text `password`.
- The Pydantic schema `UserCreate` validates the email and password format.
- The server hashes the password and stores `hashed_password` in the SQLAlchemy DB.
- The response schema `UserResponse` excludes `hashed_password` so it is NEVER 
  sent back over the internet!
==============================================================================
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# 1. Base Shared Attributes
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    is_active: Optional[bool] = True


# 2. Schema for User Registration Request (Includes Plain Password)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Plain text password for registration")


# 3. Schema for User Login Credentials
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# 4. Schema for Auth Token Response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# 5. Schema for User Public Data Response (Excludes Password!)
class UserResponse(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to serialize ORM SQLAlchemy objects
