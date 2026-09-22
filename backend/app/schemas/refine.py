"""
==============================================================================
PRE-AI Refinement Pydantic Schemas (schemas/refine.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Request and Response models for the AI Prompt Auto-Refinement Engine.

Parameters:
- `original_prompt`: Draft system or user prompt.
- `target_model`: Model family (e.g. Gemini vs Ollama Llama 3) to tailor prompt formatting.
- `optimization_goal`: "TOKEN_REDUCTION", "CLARITY", or "ACCURACY".
==============================================================================
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class RefinePromptRequest(BaseModel):
    system_prompt: Optional[str] = None
    user_prompt: str = Field(..., description="The original prompt to refine and compress")
    target_model: str = Field("gemini-1.5-flash", description="Model family to optimize for")
    optimization_goal: str = Field("TOKEN_REDUCTION", description="TOKEN_REDUCTION | CLARITY | ACCURACY")


class RefinePromptResponse(BaseModel):
    original_system_prompt: Optional[str] = None
    original_user_prompt: str
    refined_system_prompt: Optional[str] = None
    refined_user_prompt: str
    
    # Token Metrics
    original_token_count: int
    refined_token_count: int
    tokens_saved: int
    token_reduction_pct: float
    
    explanation: str = Field(..., description="Explanation of changes made for optimization")
    extracted_variables: List[str] = Field(default_factory=list)
