"""
Logs Routes - Fetch and query logs
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.database import get_db
from backend.app.models.log_model import LogEntry

router = APIRouter(prefix="/api/logs", tags=["Logs"])


@router.get("/")
async def get_logs(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    severity: Optional[str] = None,
    event_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get recent logs with optional filters"""
    try:
        query = db.query(LogEntry)
        
        if severity:
            query = query.filter(LogEntry.severity == severity)
        
        if event_type:
            query = query.filter(LogEntry.event_type == event_type)
        
        total = query.count()
        logs = query.order_by(LogEntry.timestamp.desc()).offset(offset).limit(limit).all()
        
        return {
            "success": True,
            "count": len(logs),
            "total": total,
            "logs": [
                {
                    "id": log.id,
                    "timestamp": log.timestamp.isoformat(),
                    "source_ip": log.source_ip,
                    "event_type": log.event_type,
                    "severity": log.severity,
                    "details": log.details,
                    "attack_id": log.attack_id,
                    "threat_score": log.threat_score,
                    "is_anomaly": log.is_anomaly
                }
                for log in logs
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "logs": []
        }


@router.get("/{log_id}")
async def get_log_by_id(log_id: int, db: Session = Depends(get_db)):
    """Get a single log by ID"""
    log = db.query(LogEntry).filter(LogEntry.id == log_id).first()
    
    if not log:
        return {"success": False, "message": "Log not found"}
    
    return {
        "success": True,
        "log": {
            "id": log.id,
            "timestamp": log.timestamp.isoformat(),
            "source_ip": log.source_ip,
            "event_type": log.event_type,
            "severity": log.severity,
            "details": log.details,
            "attack_id": log.attack_id,
            "threat_score": log.threat_score,
            "is_anomaly": log.is_anomaly
        }
    }
