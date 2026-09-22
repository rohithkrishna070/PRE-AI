"""
==============================================================================
PRE-AI Deployments Controller Router (api/v1/endpoints/deployments.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Promotes prompt versions to STAGING or PRODUCTION.
==============================================================================
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.deployment import DeploymentCreate, DeploymentResponse
from app.services.deployment_service import promote_to_deployment

router = APIRouter(prefix="/deployments", tags=["Deployments"])


@router.post("/", response_model=DeploymentResponse)
def promote_version(dep_in: DeploymentCreate, db: Session = Depends(get_db)):
    """
    Promotes a prompt version to Staging or Production release environment.
    """
    return promote_to_deployment(
        db, 
        prompt_id=dep_in.prompt_id, 
        prompt_version_id=dep_in.prompt_version_id, 
        environment=dep_in.environment
    )
