#!/usr/bin/env python3
"""
Database Initialization Script
Run this first to create all tables and setup the database
"""

import sys
import os

# Add parent directory to path so we can import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models.log_model import Base as LogBase
from backend.app.models.alert_model import Base as AlertBase
from backend.app.models.attack_model import Base as AttackBase
from backend.app.config import config

def init_database():
    """Initialize database with all tables"""
    print("🔧 Initializing SOC Shadow Box Database...")
    
    # Create engine
    engine = create_engine(
        config.DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {}
    )
    
    # Create all tables
    LogBase.metadata.create_all(bind=engine)
    AlertBase.metadata.create_all(bind=engine)
    AttackBase.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully!")
    print(f"📊 Database URL: {config.DATABASE_URL}")
    
    # Test connection
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        db.execute("SELECT 1")
        print("✅ Database connection test: SUCCESS")
    except Exception as e:
        print(f"❌ Database connection test: FAILED - {e}")
    finally:
        db.close()
    
    return engine

if __name__ == "__main__":
    init_database()
    print("\n🎯 Next steps:")
    print("1. Run: python database/seed_data.py (to load sample data)")
    print("2. Start backend: python backend/run.py")
    print("3. Open frontend: Open frontend/index.html in browser")
