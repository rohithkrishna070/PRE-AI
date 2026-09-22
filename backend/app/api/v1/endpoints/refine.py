"""
==============================================================================
PRE-AI Auto-Refinement Controller Router (api/v1/endpoints/refine.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Endpoint to trigger AI prompt optimization and token compression.
==============================================================================
"""

from fastapi import APIRouter
from app.schemas.refine import RefinePromptRequest, RefinePromptResponse
from app.services.refinement_service import refine_prompt

router = APIRouter(prefix="/refine", tags=["Auto-Refinement Engine"])


@router.post("/", response_model=RefinePromptResponse)
def execute_refinement(request: RefinePromptRequest):
    """
    Analyzes an unoptimized draft prompt and returns a compressed, 
    token-optimized prompt tailored for the target model.
    """
    return refine_prompt(request)
