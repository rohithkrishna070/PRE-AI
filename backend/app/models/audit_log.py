"""
==============================================================================
PRE-AI Audit Log Model (models/audit_log.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Audit Logging & Security Compliance
Audit logging records critical system events (e.g. "User created project", 
"User refined prompt v2", "User promoted version to production").

This provides an immutable trail of actions for security compliance and 
team debugging.
==============================================================================
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class AuditLog(Base):
    """
    Audit Log Entity recording user actions and system events.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Action type (e.g., "PROMPT_CREATE", "PROMPT_REFINE", "DEPLOYMENT_PROMOTED")
    action = Column(String, nullable=False, index=True)
    
    # Details description
    details = Column(Text, nullable=True)

    # Foreign Key linking to User who performed the action
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
