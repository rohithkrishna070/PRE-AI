"""
==============================================================================
PRE-AI User Database Model (models/user.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
This file defines the `User` table in the database.
In SQLAlchemy:
- `Column`: Defines a column in SQL.
- `Integer`, `String`, `Boolean`, `DateTime`: Specify column data types.
- `primary_key=True`: Uniquely identifies each row (User ID).
- `unique=True`: Ensures no two users share the same email.
- `relationship()`: Allows accessing related projects created by this user.
==============================================================================
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User(Base):
    """
    User Entity representing registered users in the platform.
    """
    __tablename__ = "users"

    # --------------------------------------------------------------------------
    # 1. Primary Key & Core Identity Fields
    # --------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    
    # --------------------------------------------------------------------------
    # 2. Authentication & Security Fields
    # --------------------------------------------------------------------------
    # Stores the secure Bcrypt password hash digest (never plain text!)
    hashed_password = Column(String, nullable=False)
    
    # User status flags
    is_active = Column(Boolean, default=True)      # Active / Suspended flag
    is_superuser = Column(Boolean, default=False)  # Admin privileges flag

    # --------------------------------------------------------------------------
    # 3. Timestamps
    # --------------------------------------------------------------------------
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --------------------------------------------------------------------------
    # 4. ORM Relationships
    # --------------------------------------------------------------------------
    # Links to projects created by this user
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    
    # Links to audit log entries performed by this user
    audit_logs = relationship("AuditLog", back_populates="user")
