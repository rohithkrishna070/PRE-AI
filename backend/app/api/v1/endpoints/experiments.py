"""
==============================================================================
PRE-AI Experiments Controller Router (api/v1/endpoints/experiments.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Multi-model benchmarking endpoints:
- Synchronous versioned experiments
- Direct ad-hoc multi-model comparisons for interactive playground
- Asynchronous experiments with FastAPI BackgroundTasks
- Historical experiment retrieval and listing
==============================================================================
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.prompt import PromptVersion
from app.models.experiment import Experiment
from app.schemas.experiment import (
    ExperimentCreate, 
    ExperimentResponse, 
    ExperimentAdHocRequest
)
from app.services.experiment_service import (
    run_experiment, 
    run_ad_hoc_experiment, 
    list_experiments, 
    get_experiment
)
from app.tasks.experiment_tasks import run_background_experiment

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.post("/", response_model=ExperimentResponse)
def create_experiment(exp_in: ExperimentCreate, db: Session = Depends(get_db)):
    """
    Executes a saved prompt version side-by-side across multiple target models synchronously.
    """
    try:
        return run_experiment(
            db=db, 
            name=exp_in.name, 
            project_id=exp_in.project_id, 
            prompt_version_id=exp_in.prompt_version_id, 
            target_models=exp_in.target_models
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/adhoc", response_model=Dict[str, Any])
def create_adhoc_experiment(request: ExperimentAdHocRequest):
    """
    Directly benchmarks any prompt across multiple models without requiring a saved prompt version.
    Ideal for real-time playground comparisons in the Experiment Arena.
    """
    return run_ad_hoc_experiment(
        prompt=request.prompt,
        target_models=request.target_models,
        system_prompt=request.system_prompt,
        name=request.name
    )


@router.post("/async", response_model=ExperimentResponse)
def create_async_experiment(
    exp_in: ExperimentCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    """
    Registers an experiment container and schedules multi-model execution in a background worker task.
    Prevents client timeout during heavy multi-model LLM benchmarking.
    """
    version = db.query(PromptVersion).filter(PromptVersion.id == exp_in.prompt_version_id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Prompt Version not found")

    experiment = Experiment(
        name=exp_in.name,
        project_id=exp_in.project_id,
        prompt_version_id=exp_in.prompt_version_id,
        target_models=exp_in.target_models
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    # Dispatch to background task worker
    background_tasks.add_task(
        run_background_experiment,
        experiment_id=experiment.id,
        prompt_text=version.user_prompt_template,
        target_models=exp_in.target_models,
        system_prompt=version.system_prompt
    )

    return experiment


@router.get("/", response_model=List[ExperimentResponse])
def get_experiments(
    project_id: Optional[int] = Query(None, description="Filter experiments by project ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Lists historical experiments with aggregated runs.
    """
    return list_experiments(db=db, project_id=project_id, skip=skip, limit=limit)


@router.get("/{experiment_id}", response_model=ExperimentResponse)
def get_experiment_details(experiment_id: int, db: Session = Depends(get_db)):
    """
    Fetches full details and benchmark run results for a specific experiment.
    """
    try:
        return get_experiment(db=db, experiment_id=experiment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
