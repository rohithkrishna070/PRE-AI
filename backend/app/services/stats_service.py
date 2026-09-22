"""
==============================================================================
PRE-AI Stats Service Entrypoint (services/stats_service.py)
------------------------------------------------------------------------------
Exposes analytics and metrics calculation helpers.
==============================================================================
"""

from app.services.deployment_service import get_platform_stats

__all__ = ["get_platform_stats"]
