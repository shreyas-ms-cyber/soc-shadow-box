"""
Replay Routes - Attack scenario recording and playback
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List
from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.database import get_db
from backend.app.services.replay_system import ReplaySystem

router = APIRouter(prefix="/api/replay", tags=["Attack Replay"])


@router.get("/scenarios")
async def list_scenarios(db: Session = Depends(get_db)):
    """Get all saved attack scenarios"""
    replay_system = ReplaySystem(db)
    scenarios = replay_system.get_all_scenarios()
    
    return {
        "success": True,
        "count": len(scenarios),
        "scenarios": scenarios
    }


@router.get("/scenario/{scenario_id}")
async def get_scenario(scenario_id: str, db: Session = Depends(get_db)):
    """Get a specific scenario by ID"""
    replay_system = ReplaySystem(db)
    scenario = replay_system.get_scenario(scenario_id)
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario {scenario_id} not found"
        )
    
    return {
        "success": True,
        "scenario": scenario
    }


@router.post("/record")
async def record_scenario(
    attack_type: str,
    steps: List[dict],
    db: Session = Depends(get_db)
):
    """Record a custom attack scenario"""
    try:
        replay_system = ReplaySystem(db)
        result = replay_system.record_attack_sequence(attack_type, steps)
        
        return {
            "success": True,
            "message": f"Scenario recorded successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record scenario: {str(e)}"
        )


@router.post("/replay/{scenario_id}")
async def replay_scenario(
    scenario_id: str,
    speed: float = 1.0,
    db: Session = Depends(get_db)
):
    """Replay a saved attack scenario"""
    try:
        replay_system = ReplaySystem(db)
        result = replay_system.replay_scenario(scenario_id, speed)
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
        
        return {
            "success": True,
            "message": f"Scenario replayed successfully at {speed}x speed",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to replay scenario: {str(e)}"
        )


@router.delete("/scenario/{scenario_id}")
async def delete_scenario(scenario_id: str, db: Session = Depends(get_db)):
    """Delete a saved scenario"""
    replay_system = ReplaySystem(db)
    deleted = replay_system.delete_scenario(scenario_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario {scenario_id} not found"
        )
    
    return {
        "success": True,
        "message": f"Scenario {scenario_id} deleted"
    }


@router.post("/demo/create")
async def create_demo_scenarios(db: Session = Depends(get_db)):
    """Create demo scenarios for testing"""
    replay_system = ReplaySystem(db)
    scenarios = replay_system.create_demo_scenarios()
    
    return {
        "success": True,
        "message": f"Created {len(scenarios)} demo scenarios",
        "scenarios": scenarios
    }
