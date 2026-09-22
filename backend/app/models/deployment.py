"""
==============================================================================
PRE-AI Deployment Database Model (models/deployment.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Production Release Management
In production software engineering, you never want your web app's frontend 
to break when someone edits a prompt draft.

Deployment decoupling:
- Your web application calls an immutable Deployment Endpoint (e.g., `/v1/deployments/customer-support-prod`).
- This endpoint routes requests to the active `PromptVersion` pinned to that environment (STAGING or PRODUCTION).
- You can promote Version 2 to Production or instantly rollback to Version 1 with zero downtime.
==============================================================================
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Deployment(Base):
    """
    Deployment Entity linking a specific PromptVersion to a release environment.
    """
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Environment name: "STAGING" or "PRODUCTION"
    environment = Column(String, default="PRODUCTION", nullable=False)
    
    # Unique deployment key string used in API endpoints
    deployment_key = Column(String, unique=True, index=True, nullable=False)

    # Foreign Keys
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)
    prompt_version_id = Column(Integer, ForeignKey("prompt_versions.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    prompt = relationship("Prompt", back_populates="deployments")
