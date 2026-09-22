"""
==============================================================================
PRE-AI Experiment Service (services/experiment_service.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Parallel Multi-Model Benchmarking
Runs a prompt version across a list of targeted models (e.g. Gemini, Ollama Llama 3) 
and records output, latency, and token consumption side-by-side.
==============================================================================
"""

from typing import List
from sqlalchemy.orm import Session
from app.models.prompt import PromptVersion
from app.models.experiment import Experiment, ExperimentRun
from app.providers.factory import get_provider


def run_experiment(
    db: Session, 
    name: str, 
    project_id: int, 
    prompt_version_id: int, 
    target_models: List[str]
) -> Experiment:
    """
    Runs a prompt version across multiple target models side-by-side.
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
        provider = get_provider(model_name)
        res = provider.generate(
            prompt=version.user_prompt_template, 
            system_prompt=version.system_prompt
        )

        run = ExperimentRun(
            experiment_id=experiment.id,
            model_name=model_name,
            output_text=res.get("text", ""),
            latency_ms=res.get("latency_ms", 0),
            prompt_tokens=res.get("prompt_tokens", 0),
            completion_tokens=res.get("completion_tokens", 0),
            status="SUCCESS"
        )
        db.add(run)

    db.commit()
    db.refresh(experiment)
    return experiment
