"""
==============================================================================
PRE-AI Prompt & Version Database Models (models/prompt.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: "GitHub for Prompts" Data Architecture
To achieve version control (like Git commit history) for AI prompts:

1. `Prompt` Entity:
   - Represents the parent repository/concept (e.g. "Support Chatbot Prompt").
   - Contains a pointer to `active_version_id` (the current live/production version).

2. `PromptVersion` Entity:
   - Represents an immutable snapshot (a "Git Commit").
   - Every time a user edits or auto-refines a prompt, a new `PromptVersion` row is created.
   - Tracks input token count, output token estimate, target model family, commit notes, 
     and parent version ID (for diff viewing).
==============================================================================
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Prompt(Base):
    """
    Parent Prompt entity representing a prompt repository/feature.
    """
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Foreign Key linking to Project
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # Pointer to the active live version
    active_version_id = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="prompts")
    versions = relationship(
        "PromptVersion", 
        back_populates="prompt", 
        foreign_keys="PromptVersion.prompt_id",
        cascade="all, delete-orphan"
    )
    deployments = relationship("Deployment", back_populates="prompt", cascade="all, delete-orphan")


class PromptVersion(Base):
    """
    Immutable Version Snapshot (Git Commit equivalent) for Prompts.
    """
    __tablename__ = "prompt_versions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key to parent Prompt
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)
    
    # Sequential Version Number (1, 2, 3...)
    version_number = Column(Integer, nullable=False)

    # Prompt Text Components
    system_prompt = Column(Text, nullable=True)   # System Role instructions
    user_prompt_template = Column(Text, nullable=False) # User prompt with {{variables}}

    # Dynamic Variables JSON (e.g. ["user_name", "query", "context"])
    variables = Column(JSON, default=list)

    # Target AI Model (e.g. "gemini-1.5-flash", "llama3:latest")
    target_model = Column(String, default="gemini-1.5-flash")

    # Token Optimization Metrics
    token_count = Column(Integer, default=0)         # Exact input token count
    token_reduction_pct = Column(Float, default=0.0) # Token savings % compared to v1

    # Git-like commit message / notes
    commit_note = Column(String, nullable=True)      # e.g. "Refined for 25% fewer tokens"

    # Link to previous parent version for diff calculations
    parent_version_id = Column(Integer, ForeignKey("prompt_versions.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    prompt = relationship("Prompt", back_populates="versions", foreign_keys=[prompt_id])
