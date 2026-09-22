"""
==============================================================================
PRE-AI Database Session & Connection Pool Manager (db/session.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
1. Engine:
   - The SQLAlchemy Engine manages the connection pool to your SQL database.
   - It sends raw SQL queries over TCP socket network connections to Postgres or SQLite.

2. Session (`SessionLocal`):
   - A Session represents a "workspace" for database transactions.
   - Whenever an API request comes in, a new Session is opened, queries are executed, 
     and the session is closed when the request finishes.

3. Resilience & Fallback:
   - We attempt to connect to PostgreSQL using your config settings.
   - If PostgreSQL is not created or running yet, we log a helpful notice 
     and fall back to local SQLite (`preai_dev.db`) so your code runs without crashing!
==============================================================================
"""

import logging
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Setup logger for database setup messages
logger = logging.getLogger("preai_db")
logging.basicConfig(level=logging.INFO)


def create_database_engine():
    """
    Attempts to create a PostgreSQL database engine connection.
    If PostgreSQL fails to connect, gracefully falls back to SQLite.
    Returns: (SQLAlchemy Engine, engine_type_string)
    """
    pg_url = settings.sync_database_url
    try:
        # Create PostgreSQL Engine with connection timeout
        engine = create_engine(
            pg_url,
            pool_pre_ping=True,      # Automatically verify live connection before executing queries
            connect_args={"connect_timeout": 3}
        )
        # Test the connection using a simple SELECT 1 query
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"✅ Successfully connected to PostgreSQL Database at: {settings.POSTGRES_SERVER}")
        return engine, "postgresql"
    except Exception as e:
        logger.warning(f"⚠️ PostgreSQL connection failed: {e}")
        logger.info(f"🔄 Falling back to local SQLite database at: {settings.SQLITE_URL}")
        
        # Create SQLite Engine (check_same_thread=False allows FastAPI multi-threading)
        engine = create_engine(
            settings.SQLITE_URL,
            connect_args={"check_same_thread": False}
        )
        return engine, "sqlite"


# Initialize the database engine
engine, ACTIVE_DB_TYPE = create_database_engine()

# Create SessionLocal class factory for database transactions
# autocommit=False: Requires explicit db.commit() for safety
# autoflush=False: Prevents premature flushing of objects to DB before commit
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    FastAPI Dependency Injector for DB Sessions.
    Yields a database session to an API route, and guarantees session closure when done.
    
    Usage in FastAPI route:
    `@app.get("/items")`
    `def read_items(db: Session = Depends(get_db)):`
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
