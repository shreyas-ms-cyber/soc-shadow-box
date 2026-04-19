from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

Base = declarative_base()

class AttackScenario(Base):
    """Database model for storing attack scenarios for replay"""
    __tablename__ = 'attack_scenarios'
    
    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    attack_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    timeline = Column(JSON, nullable=False)  # List of events
    total_steps = Column(Integer, default=0)
    duration_seconds = Column(Float, default=0.0)
    tags = Column(JSON, default=list)  # For categorization

class AttackModel(BaseModel):
    """API model for attack scenarios"""
    id: Optional[int] = None
    scenario_id: str
    name: str
    attack_type: str
    created_at: Optional[datetime] = None
    timeline: List[Dict[str, Any]]
    total_steps: int = 0
    duration_seconds: float = 0.0
    tags: List[str] = []
    
    class Config:
        from_attributes = True