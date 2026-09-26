"""
==============================================================================
PRE-AI Application Configuration Module (core/config.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
In modern web applications, configuration settings (like database passwords, 
API keys, and secret tokens) should NEVER be hardcoded into source code. 
Instead, they are loaded from Environment Variables (or a .env file).

This module uses Pydantic's `BaseSettings` which automatically:
1. Reads environment variables from your operating system or `.env` file.
2. Validates that variable types are correct (e.g., ports are integers, URLs are strings).
3. Provides default values if an environment variable is missing.
==============================================================================
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --------------------------------------------------------------------------
    # 1. Project Information & Environment
    # --------------------------------------------------------------------------
    PROJECT_NAME: str = "PRE-AI Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # --------------------------------------------------------------------------
    # 2. Security & Authentication Configuration
    # --------------------------------------------------------------------------
    # SECRET_KEY is used to digitally sign JWT tokens. Keep this secret in production!
    SECRET_KEY: str = "DEV_SUPER_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION_12345"
    
    # Algorithm used to sign the JWT token (HS256 = HMAC with SHA-256)
    ALGORITHM: str = "HS256"
    
    # How long a user login token remains valid (in minutes)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # --------------------------------------------------------------------------
    # 3. Database Connection Configuration
    # --------------------------------------------------------------------------
    # PostgreSQL Configuration details
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "Rohith@07"
    POSTGRES_DB: str = "preai_db"
    POSTGRES_PORT: str = "5432"
    
    # Primary Database URL for PostgreSQL
    # Format: postgresql://username:password@hostname:port/database_name
    DATABASE_URL: Optional[str] = None

    # SQLite Fallback URL (Used automatically if PostgreSQL is not running/created)
    SQLITE_URL: str = "sqlite:///./preai_dev.db"

    @property
    def sync_database_url(self) -> str:
        """
        Property method that constructs the Database URL.
        If DATABASE_URL environment variable is provided, it uses that.
        Otherwise, it constructs the PostgreSQL URL from individual settings.
        Uses urllib.parse.quote_plus to safely escape special characters in passwords (e.g. '@', '#').
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL
        import urllib.parse
        encoded_user = urllib.parse.quote_plus(self.POSTGRES_USER)
        encoded_password = urllib.parse.quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql://{encoded_user}:{encoded_password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # --------------------------------------------------------------------------
    # 4. AI Provider Configurations
    # --------------------------------------------------------------------------
    # Google Gemini API Key (Can be set in .env file or environment)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")

    # Ollama Local Model Server URL (Default local installation port)
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # Default target LLM model for auto-refinement
    DEFAULT_REFINEMENT_MODEL: str = "gemini-1.5-flash"

    # --------------------------------------------------------------------------
    # 5. Pydantic Settings Configuration
    # --------------------------------------------------------------------------
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instantiate a global settings object so other modules can import `settings`
settings = Settings()
