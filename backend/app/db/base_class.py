"""
==============================================================================
PRE-AI Base ORM Class (db/base_class.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
In Object-Relational Mapping (ORM) with SQLAlchemy:
- Python classes represent SQL Database Tables.
- Class instances represent Table Rows.
- Attributes represent Table Columns.

To make Python classes behave as SQL tables, they must inherit from a common 
`Base` class created by SQLAlchemy.

This module defines `Base`, which automatically assigns table names based on 
the class name (e.g. `User` class becomes `user` table in SQL).
==============================================================================
"""

from typing import Any
from sqlalchemy.orm import declarative_base, declared_attr


class CustomBase:
    """
    Base class providing automatic tablename generation.
    Converts ClassName to lowercase table_name.
    Example: `UserProfile` class -> `userprofile` table
    """
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


# DeclarativeBase factory creates the Base class for all ORM models to inherit
Base = declarative_base(cls=CustomBase)
