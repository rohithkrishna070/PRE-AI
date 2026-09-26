"""
==============================================================================
PRE-AI Prompt & Version Pydantic Schemas (schemas/prompt.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Validates creation of prompts, creation of immutable prompt versions (Git commits), 
and serialized outputs.
==============================================================================
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# ------------------------------------------------------------------------------
# 1. Prompt Version Schemas
# ------------------------------------------------------------------------------
class PromptVersionBase(BaseModel):
    system_prompt: Optional[str] = None
    user_prompt_template: str = Field(..., description="User prompt string with {{variables}}")
    variables: List[str] = Field(default_factory=list)
    target_model: str = "gemini-1.5-flash"
    commit_note: Optional[str] = "Initial commit"


class PromptVersionCreate(PromptVersionBase):
    pass


class PromptVersionResponse(PromptVersionBase):
    id: int
    prompt_id: int
    version_number: int
    token_count: int
    token_reduction_pct: float
    parent_version_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ------------------------------------------------------------------------------
# 2. Parent Prompt Schemas
# ------------------------------------------------------------------------------
class PromptBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None


class PromptCreate(PromptBase):
    project_id: int
    initial_version: PromptVersionCreate


class PromptResponse(PromptBase):
    id: int
    project_id: int
    active_version_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    versions: List[PromptVersionResponse] = []

    model_config = ConfigDict(from_attributes=True)
