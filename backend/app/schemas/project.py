"""
==============================================================================
PRE-AI Project Pydantic Schemas (schemas/project.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Schemas for validating Project Creation requests and serializing Project details.
==============================================================================
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="My AI Project")
    description: Optional[str] = Field(None, example="AI Prompts for Customer Support")


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
