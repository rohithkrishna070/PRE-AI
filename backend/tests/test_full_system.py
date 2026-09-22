"""
==============================================================================
PRE-AI Integration Test Suite (tests/test_full_system.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Automated Unit & Integration Testing
Uses `pytest` and FastAPI's `TestClient` to simulate HTTP requests without 
starting a live network server.

Tests:
1. `/health`: Health check endpoint.
2. `/api/v1/refine/`: AI Prompt Auto-Refinement engine.
==============================================================================
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """
    Tests the health check endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"


def test_prompt_refinement_api():
    """
    Tests the Prompt Auto-Refinement endpoint.
    """
    long_prompt = (
        "I would really appreciate it if you could please act as an extremely helpful "
        "and polite customer service assistant and answer the user query in a very thorough, "
        "detailed, friendly, and comprehensive manner without missing any details."
    )
    payload = {
        "user_prompt": long_prompt,
        "target_model": "gemini-1.5-flash",
        "optimization_goal": "TOKEN_REDUCTION"
    }
    response = client.post("/api/v1/refine/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "refined_user_prompt" in data
    assert "original_token_count" in data
    assert "refined_token_count" in data
