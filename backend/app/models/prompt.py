"""
==============================================================================
PRE-AI Prompt & Version Database Models (models/prompt.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: "GitHub for Prompts" Data Architecture
To achieve version control (like Git commit history) for AI prompts:

1. `Prompt` Entity:
   - Represents the parent repository/concept (e.g. "Customer Support Prompt").
   - Contains a pointer to `active_version_id` (the current live/production version).

2. `PromptVersion` Entity:
   - Represents an immutable snapshot (a "Git Commit").
   - Every time a user edits or auto-refines a prompt, a new `PromptVersion` row is created.
   - Tracks input token count, output token estimate, target model family, commit notes, 
     and parent version ID (for diff viewing).

SQLAlchemy Syntax Breakdown:
- `Column(...)`: Declares a table column in SQL.
- `Integer`, `String`, `Text`, `Float`, `JSON`, `DateTime`: Column data types.
- `primary_key=True`: Marks this column as the unique identifier (PRIMARY KEY).
- `index=True`: Creates a B-Tree search index in Postgres for faster SELECT queries.
- `nullable=False`: Equivalent to SQL `NOT NULL` (value is required).
- `ForeignKey("table.col")`: Enforces referential integrity between parent and child tables.
- `relationship(...)`: Virtual Python attribute to navigate between related tables (JOINs).
- `cascade="all, delete-orphan"`: If parent prompt is deleted, all its version rows are automatically deleted.
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

    # Syntax: primary_key=True auto-increments unique IDs (1, 2, 3...)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Syntax: String for shorter text; index=True speeds up title searching
    title = Column(String, nullable=False, index=True)
    
    # Syntax: Text allows arbitrarily long descriptions without character limits
    description = Column(Text, nullable=True)

    # Syntax: ForeignKey creates a relational constraint pointing to projects table id
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # Pointer to the currently active / deployed PromptVersion ID
    active_version_id = Column(Integer, nullable=True)

    # Timestamps: default=datetime.utcnow automatically records insertion time
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships:
    # `back_populates` links two-way communication between Project and Prompt models
    project = relationship("Project", back_populates="prompts")
    
    # `cascade="all, delete-orphan"` automatically purges versions if parent is deleted
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
    
    # Foreign Key linking this commit snapshot to its parent repository
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)
    
    # Sequential Version Number (1, 2, 3...)
    version_number = Column(Integer, nullable=False)

    # Prompt Text Components
    system_prompt = Column(Text, nullable=True)         # AI System role instructions
    user_prompt_template = Column(Text, nullable=False) # User prompt string containing {{variables}}

    # Syntax: JSON column stores structured arrays natively in PostgreSQL / SQLite
    variables = Column(JSON, default=list)

    # Target AI Model architecture: e.g. "gemini-1.5-flash", "llama3:latest"
    target_model = Column(String, default="gemini-1.5-flash")

    # Token Optimization Metrics
    token_count = Column(Integer, default=0)         # Exact input token count
    token_reduction_pct = Column(Float, default=0.0) # Token savings % compared to v1

    # Git-like commit message / notes (e.g. "Refined for 31% fewer tokens")
    commit_note = Column(String, nullable=True)

    # Syntax: Self-referential Foreign Key linking to parent version for diff calculations
    parent_version_id = Column(Integer, ForeignKey("prompt_versions.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship back to parent Prompt
    prompt = relationship("Prompt", back_populates="versions", foreign_keys=[prompt_id])
