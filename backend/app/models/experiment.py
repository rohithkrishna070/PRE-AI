"""
==============================================================================
PRE-AI Experiment Database Models (models/experiment.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Side-by-Side Model A/B Benchmarking
An Experiment runs the same prompt across MULTIPLE AI models simultaneously 
(e.g., Gemini 1.5 Flash vs Ollama Llama 3 vs Ollama Mistral) to compare:
- Output Quality
- Speed (Latency in milliseconds)
- Token Usage & Cost
==============================================================================
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Experiment(Base):
    """
    Experiment container for side-by-side model benchmarking.
    """
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)

    # Foreign Keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    prompt_version_id = Column(Integer, ForeignKey("prompt_versions.id"), nullable=False)

    # Models list to compare: ["gemini-1.5-flash", "llama3:latest", "mistral:latest"]
    target_models = Column(JSON, default=list, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="experiments")
    runs = relationship("ExperimentRun", back_populates="experiment", cascade="all, delete-orphan")


class ExperimentRun(Base):
    """
    Individual output run result for a single model in an experiment.
    """
    __tablename__ = "experiment_runs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    
    # Model name used for this run
    model_name = Column(String, nullable=False)
    
    # Execution metrics
    output_text = Column(Text, nullable=True)
    latency_ms = Column(Integer, default=0)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    status = Column(String, default="SUCCESS") # SUCCESS or ERROR

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    experiment = relationship("Experiment", back_populates="runs")
