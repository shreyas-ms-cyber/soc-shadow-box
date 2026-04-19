"""
Response Engine - Simplified Working Version
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.models.alert_model import Alert
from backend.app.config import config


class ResponseEngine:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.blocked_ips = {}
    
    def execute_response(self, alert: Alert, auto_mode: bool = True) -> Dict[str, Any]:
        if not auto_mode:
            return {"action": "manual", "message": "Manual intervention required"}
        
        if alert.threat_score >= 86:
            return self._critical_response(alert)
        elif alert.threat_score >= 61:
            return self._high_response(alert)
        else:
            return self._low_response(alert)
    
    def _critical_response(self, alert: Alert) -> Dict[str, Any]:
        actions = []
        if alert.source_ip != "MULTIPLE_IPS":
            self.blocked_ips[alert.source_ip] = datetime.utcnow() + timedelta(hours=1)
            actions.append(f"Blocked IP {alert.source_ip}")
        
        alert.status = "resolved"
        alert.response_taken = ", ".join(actions)
        alert.auto_resolved = True
        alert.resolved_at = datetime.utcnow()
        self.db_session.commit()
        
        return {"action": "critical_response", "actions_taken": actions, "message": "IP blocked"}
    
    def _high_response(self, alert: Alert) -> Dict[str, Any]:
        actions = [f"Added {alert.source_ip} to watchlist"]
        alert.status = "resolved"
        alert.response_taken = ", ".join(actions)
        alert.auto_resolved = True
        alert.resolved_at = datetime.utcnow()
        self.db_session.commit()
        
        return {"action": "high_response", "actions_taken": actions, "message": "Monitoring increased"}
    
    def _low_response(self, alert: Alert) -> Dict[str, Any]:
        actions = ["Logged for analysis"]
        alert.response_taken = ", ".join(actions)
        alert.resolved_at = datetime.utcnow()
        self.db_session.commit()
        
        return {"action": "low_response", "actions_taken": actions, "message": "Logged"}
