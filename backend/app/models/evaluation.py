"""
==============================================================================
PRE-AI Evaluation Database Models (models/evaluation.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Automated Prompt Testing
Just like software unit testing (pytest/JUnit), prompt engineering requires 
evaluating whether a new prompt version performs accurately on test cases.

1. `EvaluationDataset`: A collection of test cases (inputs and expected outputs).
2. `EvaluationResult`: Scores and outputs produced when a `PromptVersion` is 
   executed against the dataset.
==============================================================================
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class EvaluationDataset(Base):
    """
    Test Dataset entity containing test inputs and expected outputs.
    """
    __tablename__ = "evaluation_datasets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # Foreign Key to Project
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # Array of JSON test items: [{"input": "...", "expected_output": "..."}]
    test_cases = Column(JSON, default=list, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EvaluationResult(Base):
    """
    Result metrics generated when a PromptVersion is evaluated against a Dataset.
    """
    __tablename__ = "evaluation_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    prompt_version_id = Column(Integer, ForeignKey("prompt_versions.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("evaluation_datasets.id"), nullable=False)

    # Evaluation Scores (0.0 to 100.0)
    accuracy_score = Column(Float, default=0.0)      # % test cases passed
    avg_latency_ms = Column(Float, default=0.0)      # Average response speed in milliseconds
    total_tokens_used = Column(Integer, default=0)   # Total token consumption during evaluation

    # Detailed per-item output JSON: [{"test_case": 1, "output": "...", "passed": true}]
    details = Column(JSON, default=list)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
