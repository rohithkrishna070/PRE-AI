"""
==============================================================================
PRE-AI Automated Experiment & Mock Provider Test Suite
(tests/test_experiments_and_mock.py)
------------------------------------------------------------------------------
Tests:
1. Mock AI Provider token counting & response generation
2. Provider Factory routing
3. Ad-hoc playground multi-model benchmark endpoint (/api/v1/experiments/adhoc)
4. Asynchronous / Background task experiment execution
5. Experiment listing and retrieval endpoints
==============================================================================
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.providers.factory import get_provider
from app.providers.mock_provider import MockProvider
from app.tasks.experiment_tasks import run_background_experiment
from app.db.session import SessionLocal
from app.models.project import Project
from app.models.prompt import Prompt, PromptVersion
from app.models.experiment import Experiment, ExperimentRun

client = TestClient(app)


def test_mock_provider_unit():
    """Verify MockProvider token counting and text generation."""
    provider = get_provider("mock-llama3")
    assert isinstance(provider, MockProvider)
    
    text = "Analyze this customer support ticket for sentiment."
    tokens = provider.count_tokens(text)
    assert tokens > 0

    res = provider.generate(prompt=text)
    assert res["status"] == "SUCCESS"
    assert "mock-llama3" in res["model"]
    assert res["prompt_tokens"] > 0
    assert res["completion_tokens"] > 0
    assert res["latency_ms"] > 0


def test_adhoc_experiment_api():
    """Verify POST /api/v1/experiments/adhoc works without pre-saved prompts."""
    payload = {
        "name": "Test Benchmark",
        "prompt": "Summarize the quarterly incident report in 2 points.",
        "target_models": ["mock-gemini", "mock-ollama"]
    }
    response = client.post("/api/v1/experiments/adhoc", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Benchmark"
    assert len(data["runs"]) == 2
    assert "summary" in data
    assert data["summary"]["successful_models"] == 2
    assert data["summary"]["fastest_model"] in ["mock-gemini", "mock-ollama"]


def test_background_experiment_worker():
    """Verify background task creates and persists ExperimentRun records in database."""
    db = SessionLocal()
    try:
        from app.models.user import User
        # Ensure user exists for foreign key constraint
        user = db.query(User).first()
        if not user:
            user = User(email="testworker@preai.io", username="workeruser", hashed_password="hashed_pwd")
            db.add(user)
            db.commit()
            db.refresh(user)

        # Create test project and prompt
        project = Project(name="Task Test Project", description="Testing background worker", owner_id=user.id)
        db.add(project)
        db.commit()
        db.refresh(project)

        prompt = Prompt(title="Worker Prompt", project_id=project.id)
        db.add(prompt)
        db.commit()
        db.refresh(prompt)

        version = PromptVersion(
            prompt_id=prompt.id,
            version_number=1,
            user_prompt_template="Tell me a joke about {{topic}}",
            target_model="mock-1",
            token_count=10
        )
        db.add(version)
        db.commit()
        db.refresh(version)

        # Create experiment container
        experiment = Experiment(
            name="Worker Test Exp",
            project_id=project.id,
            prompt_version_id=version.id,
            target_models=["mock-model-a", "mock-model-b"]
        )
        db.add(experiment)
        db.commit()
        db.refresh(experiment)

        # Execute worker
        run_background_experiment(
            experiment_id=experiment.id,
            prompt_text=version.user_prompt_template,
            target_models=["mock-model-a", "mock-model-b"],
            system_prompt=None
        )

        # Verify runs were inserted
        runs = db.query(ExperimentRun).filter(ExperimentRun.experiment_id == experiment.id).all()
        assert len(runs) == 2
        for r in runs:
            assert r.status == "SUCCESS"
            assert r.latency_ms > 0
            assert r.prompt_tokens > 0
    finally:
        db.close()


def test_list_and_get_experiments_api():
    """Verify GET /api/v1/experiments/ and GET /api/v1/experiments/{id} endpoints."""
    # List experiments
    list_res = client.get("/api/v1/experiments/")
    assert list_res.status_code == 200
    experiments = list_res.json()
    assert isinstance(experiments, list)

    if experiments:
        exp_id = experiments[0]["id"]
        detail_res = client.get(f"/api/v1/experiments/{exp_id}")
        assert detail_res.status_code == 200
        assert detail_res.json()["id"] == exp_id
