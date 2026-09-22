"""
==============================================================================
PRE-AI Deployment & Stats Services 
(services/deployment_service.py & stats_service.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
- Deployment Service: Manages production environment keys to decouple external API calls from draft versions.
- Stats Service: Aggregates total tokens used, total tokens saved, and latency across projects.
==============================================================================
"""

import uuid
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.prompt import Prompt, PromptVersion
from app.models.deployment import Deployment
from app.models.request_log import RequestLog


# ------------------------------------------------------------------------------
# 1. Deployment Service
# ------------------------------------------------------------------------------
def promote_to_deployment(
    db: Session, prompt_id: int, prompt_version_id: int, environment: str = "PRODUCTION"
) -> Deployment:
    """
    Promotes a specific PromptVersion to a release environment (STAGING or PRODUCTION).
    Generates a static deployment_key for external API invocations.
    """
    existing = (
        db.query(Deployment)
        .filter(Deployment.prompt_id == prompt_id, Deployment.environment == environment)
        .first()
    )

    if existing:
        existing.prompt_version_id = prompt_version_id
        db.commit()
        db.refresh(existing)
        return existing

    # Create new deployment key: e.g. "dep_prod_a1b2c3d4"
    dep_key = f"dep_{environment.lower()}_{uuid.uuid4().hex[:8]}"

    deployment = Deployment(
        prompt_id=prompt_id,
        prompt_version_id=prompt_version_id,
        environment=environment,
        deployment_key=dep_key
    )
    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return deployment


# ------------------------------------------------------------------------------
# 2. Stats & Analytics Service
# ------------------------------------------------------------------------------
def get_platform_stats(db: Session) -> Dict[str, Any]:
    """
    Calculates overall platform statistics: total versions created, 
    average token reduction %, total requests logged, and average latency.
    """
    total_prompts = db.query(func.count(Prompt.id)).scalar() or 0
    total_versions = db.query(func.count(PromptVersion.id)).scalar() or 0
    
    # Calculate average token reduction % across all prompt versions
    avg_reduction = db.query(func.avg(PromptVersion.token_reduction_pct)).scalar() or 0.0
    
    total_requests = db.query(func.count(RequestLog.id)).scalar() or 0
    total_tokens = db.query(func.sum(RequestLog.total_tokens)).scalar() or 0
    avg_latency = db.query(func.avg(RequestLog.latency_ms)).scalar() or 0.0

    return {
        "total_prompts": total_prompts,
        "total_versions": total_versions,
        "avg_token_reduction_pct": round(float(avg_reduction), 2),
        "total_api_requests": total_requests,
        "total_tokens_consumed": int(total_tokens),
        "avg_latency_ms": round(float(avg_latency), 2)
    }
