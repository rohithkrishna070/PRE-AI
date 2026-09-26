"""
==============================================================================
PRE-AI Experiment Service (services/experiment_service.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Parallel Multi-Model Benchmarking
Runs prompts across a list of targeted models (e.g. Gemini, Ollama Llama 3, Mock) 
and records output, latency, and token consumption side-by-side.

Supports:
1. Versioned Experiments: Persisted against a specific PromptVersion in the database.
2. Ad-hoc Playground Experiments: Interactive benchmarking directly from the arena.
3. Asynchronous Execution: Dispatches runs in background workers.
==============================================================================
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.prompt import PromptVersion
from app.models.experiment import Experiment, ExperimentRun
from app.tasks.experiment_tasks import execute_model_run


def run_experiment(
    db: Session, 
    name: str, 
    project_id: int, 
    prompt_version_id: int, 
    target_models: List[str]
) -> Experiment:
    """
    Runs a saved prompt version across multiple target models side-by-side.
    Uses resilient error isolation per model run.
    """
    version = db.query(PromptVersion).filter(PromptVersion.id == prompt_version_id).first()
    if not version:
        raise ValueError("Prompt Version not found")

    experiment = Experiment(
        name=name,
        project_id=project_id,
        prompt_version_id=prompt_version_id,
        target_models=target_models
    )
    db.add(experiment)
    db.flush()

    for model_name in target_models:
        res = execute_model_run(
            model_name=model_name,
            prompt=version.user_prompt_template,
            system_prompt=version.system_prompt
        )

        run = ExperimentRun(
            experiment_id=experiment.id,
            model_name=model_name,
            output_text=res.get("output_text", ""),
            latency_ms=res.get("latency_ms", 0),
            prompt_tokens=res.get("prompt_tokens", 0),
            completion_tokens=res.get("completion_tokens", 0),
            status=res.get("status", "SUCCESS")
        )
        db.add(run)

    db.commit()
    db.refresh(experiment)
    return experiment


def run_ad_hoc_experiment(
    prompt: str,
    target_models: List[str],
    system_prompt: Optional[str] = None,
    name: Optional[str] = "Ad-hoc Benchmark"
) -> Dict[str, Any]:
    """
    Executes a direct ad-hoc comparison across models without requiring a saved prompt version.
    Calculates winner metrics (speed and token efficiency) for immediate UI feedback.
    """
    runs = []
    for model_name in target_models:
        run_res = execute_model_run(
            model_name=model_name,
            prompt=prompt,
            system_prompt=system_prompt
        )
        runs.append(run_res)

    successful_runs = [r for r in runs if r.get("status") == "SUCCESS"]
    fastest_model = None
    most_efficient_model = None

    if successful_runs:
        fastest_model = min(successful_runs, key=lambda x: x.get("latency_ms", 999999))["model_name"]
        most_efficient_model = min(
            successful_runs, 
            key=lambda x: x.get("prompt_tokens", 0) + x.get("completion_tokens", 0)
        )["model_name"]

    return {
        "name": name,
        "target_models": target_models,
        "runs": runs,
        "summary": {
            "total_models": len(target_models),
            "successful_models": len(successful_runs),
            "fastest_model": fastest_model,
            "most_efficient_model": most_efficient_model
        }
    }


def list_experiments(
    db: Session, 
    project_id: Optional[int] = None, 
    skip: int = 0, 
    limit: int = 50
) -> List[Experiment]:
    """
    Retrieves all benchmark experiments, optionally filtered by project.
    """
    query = db.query(Experiment)
    if project_id:
        query = query.filter(Experiment.project_id == project_id)
    return query.order_by(Experiment.created_at.desc()).offset(skip).limit(limit).all()


def get_experiment(db: Session, experiment_id: int) -> Experiment:
    """
    Retrieves a single experiment with full run records.
    """
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        raise ValueError(f"Experiment with ID {experiment_id} not found")
    return experiment
