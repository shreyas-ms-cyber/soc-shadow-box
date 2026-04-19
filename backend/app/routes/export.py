"""
Export Routes - CSV and Report Export
"""

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from datetime import datetime
import csv
import io

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.database import get_db
from backend.app.models.log_model import LogEntry

router = APIRouter(prefix="/api/export", tags=["Export"])


@router.get("/logs/csv")
async def export_logs_csv(
    limit: int = Query(1000, ge=1, le=10000),
    severity: str = None,
    db: Session = Depends(get_db)
):
    """Export logs to CSV file"""
    
    query = db.query(LogEntry)
    if severity:
        query = query.filter(LogEntry.severity == severity)
    
    logs = query.order_by(LogEntry.timestamp.desc()).limit(limit).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Timestamp', 'Source IP', 'Event Type', 'Severity', 'Details', 'Threat Score', 'Attack ID', 'Is Anomaly'])
    
    for log in logs:
        writer.writerow([
            log.timestamp.isoformat(),
            log.source_ip,
            log.event_type,
            log.severity,
            str(log.details)[:500],
            log.threat_score,
            log.attack_id or '',
            log.is_anomaly
        ])
    
    csv_content = output.getvalue()
    output.close()
    
    filename = f"logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
