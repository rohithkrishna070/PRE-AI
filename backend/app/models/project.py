"""
==============================================================================
PRE-AI Project Database Model (models/project.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Projects act as workspace containers. All prompts, evaluations, and 
experiments belong to a Project.

Key Concept - Foreign Keys:
- `owner_id = Column(Integer, ForeignKey("users.id"))`
- A Foreign Key links a row in the `projects` table to a specific user row in `users`.
- `relationship("User", back_populates="projects")` allows fetching `project.owner.username` directly in Python code.
==============================================================================
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Project(Base):
    """
    Project Workspace Entity to group prompts, evaluations, and deployments.
    """
    __tablename__ = "projects"

    # --------------------------------------------------------------------------
    # 1. Primary Key & Basic Attributes
    # --------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # --------------------------------------------------------------------------
    # 2. Foreign Key Link to User (Owner)
    # --------------------------------------------------------------------------
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # --------------------------------------------------------------------------
    # 3. Timestamps
    # --------------------------------------------------------------------------
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --------------------------------------------------------------------------
    # 4. ORM Relationships
    # --------------------------------------------------------------------------
    # Relationship back to User model
    owner = relationship("User", back_populates="projects")
    
    # Relationship to Prompts contained in this project
    prompts = relationship("Prompt", back_populates="project", cascade="all, delete-orphan")
    
    # Relationship to Experiments contained in this project
    experiments = relationship("Experiment", back_populates="project", cascade="all, delete-orphan")
