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
from pydantic import BaseModel, Field, ConfigDict


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, json_schema_extra={"example": "My AI Project"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "AI Prompts for Customer Support"})


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
