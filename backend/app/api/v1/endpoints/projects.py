"""
==============================================================================
PRE-AI Projects Controller Router (api/v1/endpoints/projects.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Provides CRUD API routes for managing workspace projects.
==============================================================================
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse)
def create_project(project_in: ProjectCreate, owner_id: int = 1, db: Session = Depends(get_db)):
    """
    Creates a new project workspace.
    """
    db_project = Project(
        name=project_in.name,
        description=project_in.description,
        owner_id=owner_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/", response_model=List[ProjectResponse])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lists all project workspaces.
    """
    return db.query(Project).offset(skip).limit(limit).all()


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """
    Gets details of a specific project workspace.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
