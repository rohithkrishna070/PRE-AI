"""
==============================================================================
PRE-AI Experiment Schemas (schemas/experiment.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Schemas for validating side-by-side multi-model experiments, ad-hoc prompt
benchmarks, and serialized experiment run outputs.
==============================================================================
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# ------------------------------------------------------------------------------
# Experiment Schemas
# ------------------------------------------------------------------------------
class ExperimentCreate(BaseModel):
    name: str
    project_id: int
    prompt_version_id: int
    target_models: List[str] = Field(default_factory=lambda: ["gemini-1.5-flash", "llama3:latest"])


class ExperimentAdHocRequest(BaseModel):
    name: Optional[str] = "Ad-hoc Benchmark"
    prompt: str = Field(..., min_length=1, description="Raw prompt text to benchmark")
    system_prompt: Optional[str] = None
    target_models: List[str] = Field(default_factory=lambda: ["gemini-1.5-flash", "llama3:latest"])


class ExperimentRunResponse(BaseModel):
    id: Optional[int] = None
    model_name: str
    output_text: Optional[str] = None
    latency_ms: int
    prompt_tokens: int
    completion_tokens: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class ExperimentResponse(BaseModel):
    id: int
    name: str
    project_id: int
    prompt_version_id: int
    target_models: List[str]
    runs: List[ExperimentRunResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
