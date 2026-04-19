from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any

Base = declarative_base()

# SQLAlchemy ORM Model for Database
class LogEntry(Base):
    """Database model for storing security logs"""
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    source_ip = Column(String(45), nullable=False)  # IPv6 ready
    event_type = Column(String(50), nullable=False)
    severity = Column(String(20), default="info")
    details = Column(JSON, nullable=False)
    attack_id = Column(String(100), nullable=True)
    is_anomaly = Column(Integer, default=0)  # 0=normal, 1=anomaly
    threat_score = Column(Float, default=0.0)
    
    # Indexes for faster queries
    __table_args__ = (
        Index('idx_timestamp', 'timestamp'),
        Index('idx_source_ip', 'source_ip'),
        Index('idx_event_type', 'event_type'),
        Index('idx_severity', 'severity'),
    )

# Pydantic Model for API (request/response validation)
class LogModel(BaseModel):
    """API model for log entries"""
    id: Optional[int] = None
    timestamp: Optional[datetime] = None
    source_ip: str
    event_type: str
    severity: str = "info"
    details: Dict[str, Any]
    attack_id: Optional[str] = None
    is_anomaly: int = 0
    threat_score: float = 0.0
    
    class Config:
        from_attributes = True  # For SQLAlchemy compatibility