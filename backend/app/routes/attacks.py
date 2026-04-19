"""
Attack Routes - API endpoints for generating and managing attacks
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List
from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.services.attack_engine import AttackSimulator
from backend.app.database import get_db  # We'll create this next

router = APIRouter(prefix="/api/attack", tags=["Attack Simulation"])


@router.post("/generate")
async def generate_attack(
    attack_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Generate a single cyber attack simulation
    
    Args:
        attack_type: Optional type of attack (brute_force, file_activity, ddos)
    
    Returns:
        Attack details and created logs
    """
    try:
        simulator = AttackSimulator(db)
        result = simulator.run_single_attack(attack_type)
        
        return {
            "success": True,
            "message": f"{attack_type or 'Random'} attack generated successfully",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate attack: {str(e)}"
        )


@router.post("/campaign")
async def generate_attack_campaign(
    attack_types: Optional[List[str]] = None,
    num_attacks: int = 3,
    db: Session = Depends(get_db)
):
    """
    Generate a campaign of multiple attacks
    
    Args:
        attack_types: List of attack types to include
        num_attacks: Number of attacks to generate
    
    Returns:
        Campaign results
    """
    try:
        simulator = AttackSimulator(db)
        results = simulator.run_campaign(attack_types, num_attacks)
        
        return {
            "success": True,
            "message": f"Campaign with {num_attacks} attacks completed",
            "data": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate campaign: {str(e)}"
        )


@router.post("/apt")
async def generate_apt_attack(db: Session = Depends(get_db)):
    """
    Generate an Advanced Persistent Threat (APT) attack - Multi-stage
    
    Returns:
        APT attack details
    """
    try:
        simulator = AttackSimulator(db)
        result = simulator.run_advanced_persistent_threat()
        
        return {
            "success": True,
            "message": "APT attack simulation completed",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate APT attack: {str(e)}"
        )


@router.get("/types")
async def get_attack_types():
    """
    Get list of available attack types
    """
    return {
        "attack_types": [
            {
                "name": "brute_force",
                "description": "Multiple failed login attempts from single IP",
                "severity": "high"
            },
            {
                "name": "file_activity",
                "description": "Suspicious file access/modification patterns",
                "severity": "critical"
            },
            {
                "name": "ddos",
                "description": "High volume traffic DDoS simulation",
                "severity": "critical"
            }
        ]
    }