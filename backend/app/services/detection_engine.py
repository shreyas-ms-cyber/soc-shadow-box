"""
Detection Engine - Simplified Working Version
"""

from datetime import datetime
from typing import Dict, Any, List, Tuple
from collections import defaultdict
from sqlalchemy.orm import Session
import json
import uuid

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.models.log_model import LogEntry
from backend.app.models.alert_model import Alert
from backend.app.config import config


class RuleBasedDetector:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def detect_threats(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        threats = []
        ip_groups = defaultdict(list)
        
        for log in logs:
            ip_groups[log.source_ip].append(log)
        
        for ip, ip_logs in ip_groups.items():
            # Check for brute force
            failed_logins = [l for l in ip_logs if l.event_type == "login_attempt" and l.details.get("status") == "failed"]
            if len(failed_logins) >= 3:
                threats.append({
                    "type": "brute_force",
                    "source_ip": ip,
                    "score": 75,
                    "details": {"failed_attempts": len(failed_logins)}
                })
            
            # Check for file activity
            file_access = [l for l in ip_logs if l.event_type == "file_activity"]
            if len(file_access) >= 5:
                threats.append({
                    "type": "suspicious_file_activity",
                    "source_ip": ip,
                    "score": 85,
                    "details": {"file_operations": len(file_access)}
                })
        
        # Check for DDoS
        api_requests = [l for l in logs if l.event_type == "api_request"]
        if len(api_requests) > 30:
            threats.append({
                "type": "ddos_attack",
                "source_ip": "MULTIPLE_IPS",
                "score": 90,
                "details": {"total_requests": len(api_requests)}
            })
        
        return threats


class AnomalyDetector:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def detect_anomalies(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        # Simple anomaly detection based on threat_score
        anomalies = []
        for log in logs:
            if log.threat_score > 80:
                anomalies.append({
                    "type": "high_threshold_anomaly",
                    "source_ip": log.source_ip,
                    "score": int(log.threat_score),
                    "details": {"event_type": log.event_type, "threat_score": log.threat_score}
                })
        return anomalies


class ThreatScorer:
    @staticmethod
    def calculate_score(rule_threats: List[Dict], ai_anomalies: List[Dict]) -> Tuple[int, str]:
        rule_scores = [t.get("score", 0) for t in rule_threats]
        ai_scores = [a.get("score", 0) for a in ai_anomalies]
        
        max_rule = max(rule_scores) if rule_scores else 0
        max_ai = max(ai_scores) if ai_scores else 0
        
        final_score = min(100, int((max_rule * 0.7) + (max_ai * 0.3)))
        
        if final_score >= 86:
            category = "Critical"
        elif final_score >= 61:
            category = "High"
        elif final_score >= 31:
            category = "Medium"
        else:
            category = "Low"
        
        return final_score, category


class DecisionEngine:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.rule_detector = RuleBasedDetector(db_session)
        self.anomaly_detector = AnomalyDetector(db_session)
        self.scorer = ThreatScorer()
    
    def analyze_and_respond(self, logs: List[LogEntry], auto_respond: bool = True) -> Dict[str, Any]:
        rule_threats = self.rule_detector.detect_threats(logs)
        ai_anomalies = self.anomaly_detector.detect_anomalies(logs)
        score, category = self.scorer.calculate_score(rule_threats, ai_anomalies)
        
        alerts_created = []
        for threat in rule_threats + ai_anomalies:
            alert = Alert(
                alert_id=f"ALT_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())[:8]}",
                source_ip=threat.get("source_ip", "unknown"),
                threat_score=float(score),
                category=category,
                description=threat.get("type", "unknown"),
                status="active",
                details=json.dumps(threat.get("details", {}))
            )
            self.db_session.add(alert)
            alerts_created.append(alert)
        
        self.db_session.commit()
        
        return {
            "analysis": {
                "rule_threats_found": len(rule_threats),
                "ai_anomalies_found": len(ai_anomalies),
                "total_threats": len(rule_threats + ai_anomalies),
                "threat_score": score,
                "threat_category": category
            },
            "alerts_created": len(alerts_created),
            "auto_response_enabled": auto_respond
        }
