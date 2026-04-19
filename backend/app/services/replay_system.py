"""
Attack Replay System - Record, store, and replay attack scenarios
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.models.attack_model import AttackScenario
from backend.app.models.log_model import LogEntry
from backend.app.services.attack_engine import AttackEngine


class ReplaySystem:
    """Handles recording and replaying attack scenarios"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.active_replays = {}  # scenario_id -> replay_state
    
    def record_attack_sequence(self, attack_type: str, steps: List[Dict]) -> Dict[str, Any]:
        """
        Record a custom attack sequence
        
        Args:
            attack_type: Type of attack (brute_force, file_activity, ddos)
            steps: List of attack steps with timing
        
        Returns:
            Saved scenario details
        """
        scenario_id = f"SCEN_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())[:8]}"
        
        # Calculate total duration
        total_duration = steps[-1].get("timestamp_offset", 0) if steps else 0
        
        scenario = AttackScenario(
            scenario_id=scenario_id,
            name=f"{attack_type.replace('_', ' ').title()} Attack - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
            attack_type=attack_type,
            timeline=steps,
            total_steps=len(steps),
            duration_seconds=total_duration,
            tags=[attack_type, "recorded"]
        )
        
        self.db_session.add(scenario)
        self.db_session.commit()
        
        return {
            "scenario_id": scenario_id,
            "name": scenario.name,
            "attack_type": attack_type,
            "total_steps": len(steps),
            "duration_seconds": total_duration
        }
    
    def get_all_scenarios(self) -> List[Dict]:
        """Get all saved attack scenarios"""
        scenarios = self.db_session.query(AttackScenario).order_by(
            desc(AttackScenario.created_at)
        ).all()
        
        return [
            {
                "scenario_id": s.scenario_id,
                "name": s.name,
                "attack_type": s.attack_type,
                "created_at": s.created_at.isoformat(),
                "total_steps": s.total_steps,
                "duration_seconds": s.duration_seconds,
                "tags": s.tags
            }
            for s in scenarios
        ]
    
    def get_scenario(self, scenario_id: str) -> Optional[Dict]:
        """Get a specific scenario by ID"""
        scenario = self.db_session.query(AttackScenario).filter(
            AttackScenario.scenario_id == scenario_id
        ).first()
        
        if not scenario:
            return None
        
        return {
            "scenario_id": scenario.scenario_id,
            "name": scenario.name,
            "attack_type": scenario.attack_type,
            "created_at": scenario.created_at.isoformat(),
            "timeline": scenario.timeline,
            "total_steps": scenario.total_steps,
            "duration_seconds": scenario.duration_seconds,
            "tags": scenario.tags
        }
    
    def replay_scenario(self, scenario_id: str, speed_multiplier: float = 1.0) -> Dict[str, Any]:
        """
        Replay a saved attack scenario
        
        Args:
            scenario_id: ID of scenario to replay
            speed_multiplier: Playback speed (0.5x, 1x, 2x, 5x)
        
        Returns:
            Replay results
        """
        scenario_data = self.get_scenario(scenario_id)
        if not scenario_data:
            return {"error": f"Scenario {scenario_id} not found"}
        
        attack_engine = AttackEngine(self.db_session)
        replayed_logs = []
        
        print(f"▶️ Replaying scenario: {scenario_data['name']}")
        print(f"   Speed: {speed_multiplier}x")
        
        for step in scenario_data["timeline"]:
            step_num = step.get("step", 0)
            action = step.get("action", "")
            
            print(f"   Step {step_num}: {action}")
            
            # Generate attack based on step
            attack_result = attack_engine.generate_attack(scenario_data["attack_type"])
            
            # Add step metadata
            attack_result["step"] = step_num
            attack_result["step_action"] = action
            attack_result["replay_id"] = f"replay_{scenario_id}_{datetime.utcnow().timestamp()}"
            
            replayed_logs.append(attack_result)
            
            # Wait for step duration (adjusted for speed)
            offset = step.get("timestamp_offset", 0)
            if offset > 0 and speed_multiplier > 0:
                import time
                wait_time = offset / speed_multiplier
                time.sleep(min(wait_time, 2))  # Cap at 2 seconds for demo
        
        return {
            "scenario_id": scenario_id,
            "scenario_name": scenario_data["name"],
            "attack_type": scenario_data["attack_type"],
            "speed_multiplier": speed_multiplier,
            "steps_replayed": len(replayed_logs),
            "logs_created": sum(r.get("logs_created", 0) for r in replayed_logs),
            "replayed_logs": replayed_logs,
            "completed_at": datetime.utcnow().isoformat()
        }
    
    def delete_scenario(self, scenario_id: str) -> bool:
        """Delete a saved scenario"""
        scenario = self.db_session.query(AttackScenario).filter(
            AttackScenario.scenario_id == scenario_id
        ).first()
        
        if scenario:
            self.db_session.delete(scenario)
            self.db_session.commit()
            return True
        return False
    
    def create_demo_scenarios(self):
        """Create demo scenarios for testing"""
        demo_scenarios = [
            {
                "attack_type": "brute_force",
                "steps": [
                    {"step": 1, "timestamp_offset": 0, "action": "Initial port scan detected", "result": "warning"},
                    {"step": 2, "timestamp_offset": 2, "action": "First login attempt: admin:admin", "result": "failed"},
                    {"step": 3, "timestamp_offset": 4, "action": "Second login attempt: root:toor", "result": "failed"},
                    {"step": 4, "timestamp_offset": 6, "action": "Rapid fire attacks (10 attempts/sec)", "result": "alert_triggered"},
                    {"step": 5, "timestamp_offset": 10, "action": "IP automatically blocked", "result": "mitigated"}
                ]
            },
            {
                "attack_type": "file_activity",
                "steps": [
                    {"step": 1, "timestamp_offset": 0, "action": "Access to /etc/passwd", "result": "logged"},
                    {"step": 2, "timestamp_offset": 3, "action": "Reading .env configuration", "result": "warning"},
                    {"step": 3, "timestamp_offset": 6, "action": "Attempt to modify database.yml", "result": "blocked"},
                    {"step": 4, "timestamp_offset": 9, "action": "Mass file encryption detected", "result": "critical_alert"},
                    {"step": 5, "timestamp_offset": 12, "action": "Process isolation triggered", "result": "contained"}
                ]
            },
            {
                "attack_type": "ddos",
                "steps": [
                    {"step": 1, "timestamp_offset": 0, "action": "Normal traffic baseline", "result": "monitoring"},
                    {"step": 2, "timestamp_offset": 3, "action": "Traffic spike +300%", "result": "warning"},
                    {"step": 3, "timestamp_offset": 6, "action": "Rate limiting engaged", "result": "mitigation"},
                    {"step": 4, "timestamp_offset": 9, "action": "Multiple IPs participating", "result": "ddos_detected"},
                    {"step": 5, "timestamp_offset": 12, "action": "Auto-scaling and traffic shaping", "result": "resolved"}
                ]
            }
        ]
        
        created = []
        for demo in demo_scenarios:
            scenario = self.record_attack_sequence(demo["attack_type"], demo["steps"])
            created.append(scenario)
        
        return created
