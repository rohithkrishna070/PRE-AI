"""
==============================================================================
PRE-AI Master v1 Router (api/v1/api.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Assembles all individual feature sub-routers (auth, projects, prompts, refine, 
experiments, deployments, audit) into a single master API router.
==============================================================================
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, projects, prompts, refine, experiments, deployments, audit

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(prompts.router)
api_router.include_router(refine.router)
api_router.include_router(experiments.router)
api_router.include_router(deployments.router)
api_router.include_router(audit.router)
