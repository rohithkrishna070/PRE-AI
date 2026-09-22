"""
==============================================================================
PRE-AI Experiments & Deployments Router (api/v1/endpoints/experiments.py & deployments.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
- Experiments: Side-by-side model comparison runner.
- Deployments: Environment promotion (Staging/Production).
==============================================================================
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.experiment import ExperimentCreate, ExperimentResponse
from app.schemas.deployment import DeploymentCreate, DeploymentResponse
from app.services.experiment_service import run_experiment
from app.services.deployment_service import promote_to_deployment

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.post("/", response_model=ExperimentResponse)
def create_experiment(exp_in: ExperimentCreate, db: Session = Depends(get_db)):
    """
    Executes a prompt version side-by-side across multiple target models.
    """
    try:
        return run_experiment(
            db, 
            name=exp_in.name, 
            project_id=exp_in.project_id, 
            prompt_version_id=exp_in.prompt_version_id, 
            target_models=exp_in.target_models
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
