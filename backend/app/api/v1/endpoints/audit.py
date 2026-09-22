"""
==============================================================================
PRE-AI Audit & Platform Stats Controller Router (api/v1/endpoints/audit.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Returns system metrics, overall token reduction %, and activity logs.
==============================================================================
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.stats_service import get_platform_stats

router = APIRouter(prefix="/audit", tags=["Analytics & Audit"])


@router.get("/stats")
def fetch_stats(db: Session = Depends(get_db)):
    """
    Returns platform-wide statistics: total prompts, average token reduction %, 
    total API requests, and average response latency.
    """
    return get_platform_stats(db)
