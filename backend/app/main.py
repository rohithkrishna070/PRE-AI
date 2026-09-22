"""
==============================================================================
PRE-AI Backend Main Entrypoint (app/main.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
This is the central entry point of the FastAPI Web Application.

What happens when Uvicorn launches this file (`uvicorn app.main:app --reload`):
1. Instantiates `FastAPI(title="PRE-AI Platform")`.
2. Sets up CORS (Cross-Origin Resource Sharing) so your React Frontend can make 
   HTTP calls to the backend without browser security blocks.
3. Automatically initializes database tables on startup.
4. Mounts the API v1 router under `/api/v1`.
==============================================================================
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.init_db import init_db
from app.api.v1.api import api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan Manager: Executes code on server startup and shutdown.
    """
    logger.info("🚀 Starting PRE-AI Backend Server...")
    # Initialize database tables
    try:
        init_db()
    except Exception as e:
        logger.warning(f"Database auto-init notice: {e}")
    yield
    logger.info("🛑 Shutting down PRE-AI Backend Server...")


# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configure CORS Middleware (Allows Frontend React app on localhost to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to specific frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount master v1 router under /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health Check"])
def root():
    """
    Root Welcome Endpoint.
    """
    return {
        "message": "Welcome to PRE-AI Platform API",
        "docs_url": "/docs",
        "version": settings.VERSION
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health Check Endpoint for load balancers and monitoring.
    """
    return {"status": "HEALTHY", "platform": settings.PROJECT_NAME}
