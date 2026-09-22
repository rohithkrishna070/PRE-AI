"""
==============================================================================
PRE-AI Automated Evaluation & Benchmarking Services 
(services/evaluation_service.py & experiment_service.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
- Evaluation Engine: Batch tests a PromptVersion against test cases and records accuracy/latency.
- Experiment Engine: Runs a PromptVersion concurrently across multiple models (e.g. Gemini vs Ollama).
==============================================================================
"""

import time
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.prompt import PromptVersion
from app.models.evaluation import EvaluationDataset, EvaluationResult
from app.models.experiment import Experiment, ExperimentRun
from app.providers.factory import get_provider


def run_evaluation(
    db: Session, prompt_version_id: int, dataset_id: int
) -> EvaluationResult:
    """
    Executes a PromptVersion against all test cases in an EvaluationDataset.
    Calculates accuracy score, average latency, and total tokens used.
    """
    version = db.query(PromptVersion).filter(PromptVersion.id == prompt_version_id).first()
    dataset = db.query(EvaluationDataset).filter(EvaluationDataset.id == dataset_id).first()

    if not version or not dataset:
        raise ValueError("Prompt Version or Evaluation Dataset not found")

    provider = get_provider(version.target_model)
    test_cases = dataset.test_cases or []

    passed_count = 0
    total_latency_ms = 0
    total_tokens = 0
    results_details = []

    for idx, case in enumerate(test_cases):
        input_data = case.get("input", "")
        expected = case.get("expected_output", "")

        # Substitute variable if template contains {{input}}
        prompt_text = version.user_prompt_template.replace("{{input}}", input_data)
        
        # Execute AI Provider
        res = provider.generate(prompt=prompt_text, system_prompt=version.system_prompt)
        output_text = res.get("text", "")
        
        latency = res.get("latency_ms", 0)
        tokens = res.get("prompt_tokens", 0) + res.get("completion_tokens", 0)

        total_latency_ms += latency
        total_tokens += tokens

        # Simple pass condition: expected string contained in output (or mock pass)
        passed = (expected.lower() in output_text.lower()) if expected else True
        if passed:
            passed_count += 1

        results_details.append({
            "test_case_index": idx + 1,
            "input": input_data,
            "expected_output": expected,
            "actual_output": output_text,
            "latency_ms": latency,
            "tokens": tokens,
            "passed": passed
        })

    total_cases = len(test_cases) or 1
    accuracy_score = round((passed_count / total_cases) * 100.0, 2)
    avg_latency = round(total_latency_ms / total_cases, 2)

    db_result = EvaluationResult(
        prompt_version_id=prompt_version_id,
        dataset_id=dataset_id,
        accuracy_score=accuracy_score,
        avg_latency_ms=avg_latency,
        total_tokens_used=total_tokens,
        details=results_details
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
