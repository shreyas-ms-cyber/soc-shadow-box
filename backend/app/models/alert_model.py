from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json

Base = declarative_base()

class Alert(Base):
    """Database model for security alerts"""
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(100), unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    source_ip = Column(String(45), nullable=False)
    threat_score = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(20), default="active")
    response_taken = Column(Text, nullable=True)  # Changed to Text
    resolved_at = Column(DateTime, nullable=True)
    auto_resolved = Column(Boolean, default=False)
    details = Column(Text, default="{}")  # JSON string

class AlertModel(BaseModel):
    """API model for alerts"""
    id: Optional[int] = None
    alert_id: str
    timestamp: Optional[datetime] = None
    source_ip: str
    threat_score: float
    category: str
    description: str
    status: str = "active"
    response_taken: Optional[str] = None
    resolved_at: Optional[datetime] = None
    auto_resolved: bool = False
    details: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True
