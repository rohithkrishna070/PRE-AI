"""
==============================================================================
PRE-AI Request Log Model (models/request_log.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Analytics & Token Usage Tracking
Every time an AI model generates text or executes a prompt:
- We log the prompt token count, completion token count, and total execution latency.
- This feeds the Stats & Analytics dashboard to show token savings percentages and cost metrics.
==============================================================================
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from app.db.base_class import Base


class RequestLog(Base):
    """
    Request Log Entity tracking token counts, latency, and cost per execution.
    """
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Model used for execution
    model_name = Column(String, nullable=False, index=True)

    # Foreign Key linking to prompt version if applicable
    prompt_version_id = Column(Integer, ForeignKey("prompt_versions.id"), nullable=True)

    # Token & Metric Counters
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    latency_ms = Column(Float, default=0.0)
    estimated_cost_usd = Column(Float, default=0.0)

    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
