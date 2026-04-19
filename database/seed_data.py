#!/usr/bin/env python3
"""
Seed Database with Sample Attack Data
Populates the database with realistic attack scenarios for testing
"""

import sys
import os
import random
from datetime import datetime, timedelta

# Add parent directory to path so we can import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.init_db import init_database
from backend.app.models.log_model import LogEntry
from backend.app.models.alert_model import Alert
from backend.app.models.attack_model import AttackScenario

def generate_sample_logs(session: Session, count: int = 50):
    """Generate sample log entries"""
    print(f"📝 Generating {count} sample logs...")
    
    event_types = ["login_attempt", "file_access", "api_request", "config_change"]
    severities = ["info", "warning", "error", "critical"]
    ips = [f"192.168.1.{i}" for i in range(1, 21)] + [f"10.0.0.{i}" for i in range(1, 11)]
    
    logs = []
    for i in range(count):
        timestamp = datetime.utcnow() - timedelta(hours=random.randint(0, 24))
        
        log = LogEntry(
            timestamp=timestamp,
            source_ip=random.choice(ips),
            event_type=random.choice(event_types),
            severity=random.choice(severities),
            details={
                "user": f"user_{random.randint(1, 50)}",
                "status": random.choice(["success", "failed", "pending"]),
                "request_id": f"req_{random.randint(1000, 9999)}",
                "user_agent": "Mozilla/5.0 (Sample Data)"
            },
            attack_id=f"attack_{random.randint(1, 10)}" if random.random() > 0.7 else None,
            is_anomaly=random.choice([0, 0, 0, 1]),
            threat_score=random.uniform(0, 100)
        )
        logs.append(log)
    
    session.bulk_save_objects(logs)
    session.commit()
    print(f"✅ Added {len(logs)} sample logs")

def generate_sample_alerts(session: Session, count: int = 20):
    """Generate sample alerts"""
    print(f"🚨 Generating {count} sample alerts...")
    
    categories = ["Low", "Medium", "High", "Critical"]
    statuses = ["active", "resolved", "false_positive"]
    descriptions = [
        "Multiple failed login attempts detected",
        "Suspicious file access pattern",
        "Unusual traffic volume from single IP",
        "Potential brute force attack in progress",
        "Anomalous behavior detected by AI",
        "Rate limit exceeded for API endpoint"
    ]
    
    alerts = []
    for i in range(count):
        threat_score = random.uniform(0, 100)
        category = categories[min(int(threat_score / 25), 3)]
        
        alert = Alert(
            alert_id=f"ALT_{datetime.utcnow().strftime('%Y%m%d')}_{i:04d}",
            timestamp=datetime.utcnow() - timedelta(hours=random.randint(0, 48)),
            source_ip=f"192.168.1.{random.randint(1, 50)}",
            threat_score=threat_score,
            category=category,
            description=random.choice(descriptions),
            status=random.choice(statuses),
            response_taken=f"Blocked IP for 1 hour" if random.random() > 0.5 else None,
            auto_resolved=random.choice([True, False])
        )
        alerts.append(alert)
    
    session.bulk_save_objects(alerts)
    session.commit()
    print(f"✅ Added {len(alerts)} sample alerts")

def generate_sample_attack_scenarios(session: Session):
    """Generate sample attack scenarios for replay feature"""
    print("🎯 Generating sample attack scenarios...")
    
    scenarios = [
        {
            "scenario_id": "SCEN_BRUTE_001",
            "name": "SSH Brute Force Attack",
            "attack_type": "brute_force",
            "timeline": [
                {"step": 1, "timestamp_offset": 0, "action": "Initial connection attempt", "result": "failed"},
                {"step": 2, "timestamp_offset": 2, "action": "Login attempt with admin:password123", "result": "failed"},
                {"step": 3, "timestamp_offset": 4, "action": "Login attempt with root:toor", "result": "failed"},
                {"step": 4, "timestamp_offset": 6, "action": "10 more failed attempts in rapid succession", "result": "blocked"},
                {"step": 5, "timestamp_offset": 10, "action": "System detects anomaly", "result": "IP blacklisted"}
            ],
            "total_steps": 5,
            "duration_seconds": 10.0,
            "tags": ["brute_force", "ssh", "authentication"]
        },
        {
            "scenario_id": "SCEN_DDOS_001",
            "name": "DDoS Simulation",
            "attack_type": "ddos",
            "timeline": [
                {"step": 1, "timestamp_offset": 0, "action": "Normal traffic pattern", "result": "baseline"},
                {"step": 2, "timestamp_offset": 5, "action": "Traffic increases 500%", "result": "warning"},
                {"step": 3, "timestamp_offset": 10, "action": "Rate limiting engaged", "result": "mitigation"},
                {"step": 4, "timestamp_offset": 15, "action": "AI detects anomaly", "result": "alert_triggered"},
                {"step": 5, "timestamp_offset": 20, "action": "Auto-scaling and traffic shaping", "result": "contained"}
            ],
            "total_steps": 5,
            "duration_seconds": 20.0,
            "tags": ["ddos", "network", "traffic"]
        }
    ]
    
    for scenario_data in scenarios:
        scenario = AttackScenario(
            scenario_id=scenario_data["scenario_id"],
            name=scenario_data["name"],
            attack_type=scenario_data["attack_type"],
            timeline=scenario_data["timeline"],
            total_steps=scenario_data["total_steps"],
            duration_seconds=scenario_data["duration_seconds"],
            tags=scenario_data["tags"]
        )
        session.add(scenario)
    
    session.commit()
    print(f"✅ Added {len(scenarios)} attack scenarios")

def main():
    """Main seeding function"""
    print("🌱 Seeding database with sample data...")
    
    # Initialize database
    engine = init_database()
    session = Session(engine)
    
    try:
        generate_sample_logs(session, 50)
        generate_sample_alerts(session, 20)
        generate_sample_attack_scenarios(session)
        
        print("\n✅ Database seeding completed successfully!")
        
        log_count = session.query(LogEntry).count()
        alert_count = session.query(Alert).count()
        scenario_count = session.query(AttackScenario).count()
        
        print(f"\n📊 Database Statistics:")
        print(f"   - Logs: {log_count}")
        print(f"   - Alerts: {alert_count}")
        print(f"   - Attack Scenarios: {scenario_count}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
