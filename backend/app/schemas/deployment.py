"""
==============================================================================
PRE-AI Deployment Schemas (schemas/deployment.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Schemas for promoting prompt versions to STAGING or PRODUCTION.
==============================================================================
"""

from datetime import datetime
from pydantic import BaseModel, Field


class DeploymentCreate(BaseModel):
    prompt_id: int
    prompt_version_id: int
    environment: str = Field("PRODUCTION", description="STAGING | PRODUCTION")


class DeploymentResponse(BaseModel):
    id: int
    environment: str
    deployment_key: str
    prompt_id: int
    prompt_version_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
