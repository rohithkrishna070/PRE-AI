"""
==============================================================================
PRE-AI Background Experiment Tasks (tasks/experiment_tasks.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Asynchronous Multi-Model Benchmark Execution
Running large prompts across multiple LLMs (e.g. Google Gemini 1.5, Ollama Llama 3)
can take several seconds. To prevent HTTP connection timeouts and avoid blocking
the client thread, experiments can be dispatched to background tasks.

This worker task:
1. Opens an isolated database session.
2. Iterates over each target model.
3. Invokes the provider with error isolation (one failing model doesn't fail the whole job).
4. Records latency, token consumption, and model output in real time.
==============================================================================
"""

import logging
from typing import List, Optional
from app.db.session import SessionLocal
from app.models.experiment import Experiment, ExperimentRun
from app.providers.factory import get_provider

logger = logging.getLogger("experiment_tasks")


def execute_model_run(model_name: str, prompt: str, system_prompt: Optional[str] = None) -> dict:
    """
    Executes a single model completion with exception handling and latency tracking.
    """
    try:
        provider = get_provider(model_name)
        res = provider.generate(prompt=prompt, system_prompt=system_prompt)
        return {
            "model_name": model_name,
            "output_text": res.get("text", ""),
            "latency_ms": res.get("latency_ms", 0),
            "prompt_tokens": res.get("prompt_tokens", 0),
            "completion_tokens": res.get("completion_tokens", 0),
            "status": "SUCCESS"
        }
    except Exception as exc:
        logger.error(f"Error running model '{model_name}': {exc}", exc_info=True)
        return {
            "model_name": model_name,
            "output_text": f"Error executing model completion: {str(exc)}",
            "latency_ms": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "status": "ERROR"
        }


def run_background_experiment(
    experiment_id: int, 
    prompt_text: str, 
    target_models: List[str], 
    system_prompt: Optional[str] = None
):
    """
    Background worker executed via FastAPI BackgroundTasks.
    Runs each model and commits ExperimentRun records to the database.
    """
    logger.info(f"🚀 Starting background experiment #{experiment_id} across {len(target_models)} models...")
    db = SessionLocal()
    try:
        experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
        if not experiment:
            logger.error(f"Experiment #{experiment_id} not found in database.")
            return

        for model_name in target_models:
            result = execute_model_run(model_name, prompt_text, system_prompt)
            run = ExperimentRun(
                experiment_id=experiment.id,
                model_name=result["model_name"],
                output_text=result["output_text"],
                latency_ms=result["latency_ms"],
                prompt_tokens=result["prompt_tokens"],
                completion_tokens=result["completion_tokens"],
                status=result["status"]
            )
            db.add(run)
            db.commit()
            logger.info(f"✅ Completed run for '{model_name}' on experiment #{experiment_id} (Status: {result['status']})")

        logger.info(f"✨ Successfully finished background experiment #{experiment_id}")
    except Exception as e:
        logger.error(f"Unexpected error in background experiment #{experiment_id}: {e}", exc_info=True)
    finally:
        db.close()
