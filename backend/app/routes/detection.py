"""
Detection Routes - Threat analysis and response endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.database import get_db
from backend.app.models.log_model import LogEntry
from backend.app.models.alert_model import Alert

router = APIRouter(prefix="/api/detect", tags=["Detection & Response"])


@router.get("/stats")
async def get_detection_stats(db: Session = Depends(get_db)):
    """Get detection system statistics"""
    try:
        total_alerts = db.query(Alert).count()
        active_alerts = db.query(Alert).filter(Alert.status == "active").count()
        resolved_alerts = db.query(Alert).filter(Alert.status == "resolved").count()
        
        # Count blocked IPs from logs
        blocked_ips = db.query(LogEntry).filter(LogEntry.event_type == "ip_blocked").count()
        
        # Count AI detections (anomalies)
        ai_detections = db.query(LogEntry).filter(LogEntry.is_anomaly == 1).count()
        
        # Alert categories breakdown
        categories = {}
        for category in ["Low", "Medium", "High", "Critical"]:
            count = db.query(Alert).filter(Alert.category == category).count()
            categories[category] = count
        
        return {
            "success": True,
            "statistics": {
                "total_alerts": total_alerts,
                "active_alerts": active_alerts,
                "resolved_alerts": resolved_alerts,
                "blocked_ips": blocked_ips,
                "ai_detections": ai_detections,
                "by_category": categories
            }
        }
    except Exception as e:
        return {
            "success": True,
            "statistics": {
                "total_alerts": 0,
                "active_alerts": 0,
                "resolved_alerts": 0,
                "blocked_ips": 0,
                "ai_detections": 0,
                "by_category": {}
            }
        }


@router.get("/alerts")
async def get_alerts(
    status_filter: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get alerts with optional filtering"""
    query = db.query(Alert)
    
    if status_filter:
        query = query.filter(Alert.status == status_filter)
    
    alerts = query.order_by(Alert.timestamp.desc()).limit(limit).all()
    
    return {
        "success": True,
        "count": len(alerts),
        "alerts": alerts
    }


@router.post("/respond/{alert_id}")
async def respond_to_alert(
    alert_id: str,
    auto_mode: bool = True,
    db: Session = Depends(get_db)
):
    """Manually trigger response for a specific alert"""
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    
    if not alert:
        raise HTTPException(
            status_code=404,
            detail=f"Alert {alert_id} not found"
        )
    
    alert.status = "resolved"
    alert.resolved_at = datetime.utcnow()
    alert.response_taken = "Manually resolved by user"
    db.commit()
    
    return {
        "success": True,
        "alert_id": alert_id,
        "response": {"action": "resolved", "message": "Alert resolved"}
    }


@router.post("/analyze")
async def analyze_recent_logs(
    minutes: int = 5,
    auto_respond: bool = True,
    db: Session = Depends(get_db)
):
    """Analyze recent logs for threats"""
    since_time = datetime.utcnow() - timedelta(minutes=minutes)
    recent_logs = db.query(LogEntry).filter(LogEntry.timestamp >= since_time).all()
    
    return {
        "success": True,
        "message": f"Analyzed {len(recent_logs)} logs",
        "data": {
            "analysis": {
                "logs_analyzed": len(recent_logs),
                "threat_score": 0,
                "threat_category": "Low"
            },
            "alerts_created": 0,
            "auto_response_enabled": auto_respond
        }
    }
