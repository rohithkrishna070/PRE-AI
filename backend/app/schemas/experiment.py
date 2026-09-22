"""
==============================================================================
PRE-AI Experiment & Deployment Schemas (schemas/experiment.py & deployment.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Schemas for validating side-by-side model experiments and production deployments.
==============================================================================
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ------------------------------------------------------------------------------
# Experiment Schemas
# ------------------------------------------------------------------------------
class ExperimentCreate(BaseModel):
    name: str
    project_id: int
    prompt_version_id: int
    target_models: List[str] = Field(default_factory=lambda: ["gemini-1.5-flash", "llama3:latest"])


class ExperimentRunResponse(BaseModel):
    id: int
    model_name: str
    output_text: Optional[str] = None
    latency_ms: int
    prompt_tokens: int
    completion_tokens: int
    status: str

    class Config:
        from_attributes = True


class ExperimentResponse(BaseModel):
    id: int
    name: str
    project_id: int
    prompt_version_id: int
    target_models: List[str]
    runs: List[ExperimentRunResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
