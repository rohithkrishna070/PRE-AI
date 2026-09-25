"""
==============================================================================
PRE-AI Prompts Controller Router (api/v1/endpoints/prompts.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Handles prompt creation, version committing, and version retrieval.

Syntax Breakdown:
- `@router.post(...)` / `@router.get(...)`: FastAPI route decorators binding HTTP methods.
- `response_model=PromptResponse`: Pydantic schema automatically serializing outgoing JSON.
- `db: Session = Depends(get_db)`: FastAPI Dependency Injection providing an open DB session.
- `raise HTTPException(status_code=404, ...)`: Returns a standardized JSON error response.
==============================================================================
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.prompt import Prompt, PromptVersion
from app.schemas.prompt import PromptCreate, PromptResponse, PromptVersionCreate, PromptVersionResponse
from app.services.prompt_service import create_prompt_with_initial_version, create_new_prompt_version

# Syntax: APIRouter groups endpoints under a common prefix and Swagger tag
router = APIRouter(prefix="/prompts", tags=["Prompts"])


@router.post("/", response_model=PromptResponse)
def create_prompt(prompt_in: PromptCreate, db: Session = Depends(get_db)):
    """
    Functionality:
    Creates a new prompt repository along with its initial Version 1 snapshot.

    Syntax:
    - `prompt_in: PromptCreate`: Pydantic schema validating the incoming JSON body.
    - `db: Session = Depends(get_db)`: Injects an active PostgreSQL session.
    """
    return create_prompt_with_initial_version(db, prompt_in)


@router.get("/", response_model=List[PromptResponse])
def list_prompts(project_id: int = None, db: Session = Depends(get_db)):
    """
    Functionality:
    Lists all prompt repositories, optionally filtered by project_id query parameter.

    Syntax:
    - `db.query(Prompt)`: SQLAlchemy query builder executing `SELECT * FROM prompts`.
    """
    query = db.query(Prompt)
    if project_id:
        query = query.filter(Prompt.project_id == project_id)
    return query.all()


@router.get("/{prompt_id}", response_model=PromptResponse)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """
    Functionality:
    Retrieves full details and version history of a prompt repository.

    Syntax:
    - `{prompt_id}`: Path parameter captured from the URL.
    - `.first()`: Returns the first matching SQLAlchemy object or None.
    """
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.post("/{prompt_id}/versions", response_model=PromptVersionResponse)
def add_version(prompt_id: int, version_in: PromptVersionCreate, db: Session = Depends(get_db)):
    """
    Functionality:
    Commits a new version snapshot to an existing prompt (Git Commit equivalent).

    Syntax:
    - `try/except ValueError`: Catches business logic errors and maps them to HTTP 404.
    """
    try:
        return create_new_prompt_version(db, prompt_id, version_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
