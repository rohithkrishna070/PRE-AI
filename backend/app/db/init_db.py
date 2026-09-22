"""
==============================================================================
PRE-AI Database Initialization Script (db/init_db.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Automatic Table Creation
This script imports the SQLAlchemy `Base` and all ORM models (`User`, `Project`, 
`Prompt`, `PromptVersion`, `EvaluationDataset`, `Experiment`, `Deployment`, etc.).

When `Base.metadata.create_all(bind=engine)` runs:
1. It inspects all Python model classes.
2. It generates and executes the corresponding SQL `CREATE TABLE IF NOT EXISTS` 
   queries on PostgreSQL or SQLite automatically!

Usage:
`python -m app.db.init_db`
==============================================================================
"""

import logging
from app.db.session import engine, ACTIVE_DB_TYPE
from app.db.base_class import Base

# Import all models so SQLAlchemy metadata registers them before creating tables
from app.models.user import User
from app.models.project import Project
from app.models.prompt import Prompt, PromptVersion
from app.models.evaluation import EvaluationDataset, EvaluationResult
from app.models.experiment import Experiment, ExperimentRun
from app.models.deployment import Deployment
from app.models.request_log import RequestLog
from app.models.audit_log import AuditLog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_db")


def init_db():
    """
    Creates all database tables in the active database engine.
    """
    logger.info(f"🚀 Initializing database tables on [{ACTIVE_DB_TYPE.upper()}] engine...")
    try:
        # Generate all SQL tables
        Base.metadata.create_all(bind=engine)
        logger.info("✨ All database tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Error initializing database tables: {e}")
        raise e


if __name__ == "__main__":
    init_db()
