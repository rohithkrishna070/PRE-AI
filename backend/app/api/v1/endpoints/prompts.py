"""
==============================================================================
PRE-AI Prompts Controller Router (api/v1/endpoints/prompts.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Handles prompt creation, version committing, and version retrieval.
==============================================================================
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.prompt import Prompt, PromptVersion
from app.schemas.prompt import PromptCreate, PromptResponse, PromptVersionCreate, PromptVersionResponse
from app.services.prompt_service import create_prompt_with_initial_version, create_new_prompt_version

router = APIRouter(prefix="/prompts", tags=["Prompts"])


@router.post("/", response_model=PromptResponse)
def create_prompt(prompt_in: PromptCreate, db: Session = Depends(get_db)):
    """
    Creates a new prompt repository with Version 1.
    """
    return create_prompt_with_initial_version(db, prompt_in)


@router.get("/", response_model=List[PromptResponse])
def list_prompts(project_id: int = None, db: Session = Depends(get_db)):
    """
    Lists all prompts, optionally filtered by project_id.
    """
    query = db.query(Prompt)
    if project_id:
        query = query.filter(Prompt.project_id == project_id)
    return query.all()


@router.get("/{prompt_id}", response_model=PromptResponse)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """
    Retrieves details and version history of a prompt.
    """
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.post("/{prompt_id}/versions", response_model=PromptVersionResponse)
def add_version(prompt_id: int, version_in: PromptVersionCreate, db: Session = Depends(get_db)):
    """
    Commits a new version snapshot to an existing prompt (Git Commit equivalent).
    """
    try:
        return create_new_prompt_version(db, prompt_id, version_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
