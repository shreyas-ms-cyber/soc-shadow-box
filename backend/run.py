#!/usr/bin/env python3
"""
Entry point for the SOC Shadow Box Backend Server
Run this to start the FastAPI server
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from backend.app.config import config

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════╗
    ║   SOC SHADOW BOX - AI Cyber Defense      ║
    ║         Starting Backend Server           ║
    ╚═══════════════════════════════════════════╝
    """)
    
    print(f"🔧 Configuration:")
    print(f"   - API Port: {config.API_PORT}")
    print(f"   - Database: {config.DATABASE_URL}")
    print(f"   - Auto Response: {config.AUTO_RESPONSE_ENABLED}")
    print(f"   - WebSocket: {config.WEBSOCKET_ENABLED}")
    
    print("\n🚀 Starting Uvicorn server...")
    print(f"📡 API Docs will be available at: http://localhost:{config.API_PORT}/docs")
    print("⚠️  Press CTRL+C to stop the server\n")
    
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=config.API_PORT,
        reload=True,
        log_level=config.LOG_LEVEL.lower()
    )
