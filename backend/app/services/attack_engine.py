"""
Shadow Attack Engine - Simplified Working Version
"""

import random
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.models.log_model import LogEntry


class AttackEngine:
    """Generates simulated cyber attacks"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def generate_attack(self, attack_type: str = None) -> Dict[str, Any]:
        """Generate a single attack"""
        if attack_type is None:
            attack_type = random.choice(["brute_force", "file_activity", "ddos"])
        
        if attack_type == "brute_force":
            return self._generate_brute_force()
        elif attack_type == "file_activity":
            return self._generate_file_activity()
        elif attack_type == "ddos":
            return self._generate_ddos()
        else:
            raise ValueError(f"Unknown attack type: {attack_type}")
    
    def _generate_brute_force(self) -> Dict[str, Any]:
        """Generate brute force attack"""
        attack_id = str(uuid.uuid4())
        source_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
        failed_attempts = random.randint(5, 15)
        
        logs_created = 0
        for i in range(failed_attempts):
            log = LogEntry(
                timestamp=datetime.utcnow(),
                source_ip=source_ip,
                event_type="login_attempt",
                severity="warning" if i > 5 else "info",
                details={
                    "username": random.choice(["admin", "root", "user", "test"]),
                    "status": "failed",
                    "attempt": i + 1
                },
                attack_id=attack_id,
                is_anomaly=1,
                threat_score=random.uniform(60, 95)
            )
            self.db_session.add(log)
            logs_created += 1
        
        self.db_session.commit()
        
        return {
            "attack_id": attack_id,
            "attack_type": "brute_force",
            "timestamp": datetime.utcnow().isoformat(),
            "source_ip": source_ip,
            "severity": "high",
            "description": f"Brute force attack from {source_ip} with {failed_attempts} attempts",
            "details": {"failed_attempts": failed_attempts},
            "logs_created": logs_created
        }
    
    def _generate_file_activity(self) -> Dict[str, Any]:
        """Generate file activity attack"""
        attack_id = str(uuid.uuid4())
        source_ip = f"10.0.{random.randint(1, 50)}.{random.randint(1, 255)}"
        
        sensitive_files = ["/etc/passwd", ".env", "credentials.txt", "config.php", "database.yml"]
        num_operations = random.randint(3, 10)
        
        logs_created = 0
        for i in range(num_operations):
            log = LogEntry(
                timestamp=datetime.utcnow(),
                source_ip=source_ip,
                event_type="file_activity",
                severity="high",
                details={
                    "file": random.choice(sensitive_files),
                    "operation": random.choice(["read", "modify", "copy"]),
                    "user": f"process_{random.randint(1000, 9999)}"
                },
                attack_id=attack_id,
                is_anomaly=1,
                threat_score=random.uniform(70, 98)
            )
            self.db_session.add(log)
            logs_created += 1
        
        self.db_session.commit()
        
        return {
            "attack_id": attack_id,
            "attack_type": "file_activity",
            "timestamp": datetime.utcnow().isoformat(),
            "source_ip": source_ip,
            "severity": "critical",
            "description": f"Suspicious file activity from {source_ip}",
            "details": {"operations": num_operations},
            "logs_created": logs_created
        }
    
    def _generate_ddos(self) -> Dict[str, Any]:
        """Generate DDoS attack"""
        attack_id = str(uuid.uuid4())
        num_requests = random.randint(50, 150)
        unique_ips = random.randint(5, 20)
        
        logs_created = 0
        for i in range(min(num_requests, 50)):  # Limit to 50 logs for performance
            log = LogEntry(
                timestamp=datetime.utcnow(),
                source_ip=f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                event_type="api_request",
                severity="high",
                details={
                    "endpoint": random.choice(["/api/login", "/api/data", "/", "/api/search"]),
                    "method": "GET",
                    "status_code": random.choice([200, 429, 500])
                },
                attack_id=attack_id,
                is_anomaly=1,
                threat_score=random.uniform(80, 99)
            )
            self.db_session.add(log)
            logs_created += 1
        
        self.db_session.commit()
        
        return {
            "attack_id": attack_id,
            "attack_type": "ddos",
            "timestamp": datetime.utcnow().isoformat(),
            "source_ip": "MULTIPLE_IPS",
            "severity": "critical",
            "description": f"DDoS attack detected: {num_requests} requests from {unique_ips} IPs",
            "details": {"total_requests": num_requests, "unique_ips": unique_ips},
            "logs_created": logs_created
        }


class AttackSimulator:
    """High-level simulator for attacks"""
    
    def __init__(self, db_session: Session):
        self.engine = AttackEngine(db_session)
    
    def run_single_attack(self, attack_type: str = None) -> Dict[str, Any]:
        return self.engine.generate_attack(attack_type)
    
    def run_campaign(self, attack_types: List[str] = None, num_attacks: int = 3) -> List[Dict[str, Any]]:
        if attack_types is None:
            attack_types = ["brute_force", "file_activity", "ddos"]
        
        results = []
        for i in range(num_attacks):
            attack_type = random.choice(attack_types)
            result = self.engine.generate_attack(attack_type)
            result["campaign_step"] = i + 1
            results.append(result)
        
        return results
    
    def run_advanced_persistent_threat(self) -> Dict[str, Any]:
        recon = self.engine.generate_attack("file_activity")
        brute = self.engine.generate_attack("brute_force")
        ddos = self.engine.generate_attack("ddos")
        
        return {
            "apt_attack_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "stages": {"reconnaissance": recon, "credential_attack": brute, "distraction": ddos},
            "total_logs_generated": recon["logs_created"] + brute["logs_created"] + ddos["logs_created"],
            "severity": "critical",
            "description": "APT detected - Multi-stage attack"
        }
