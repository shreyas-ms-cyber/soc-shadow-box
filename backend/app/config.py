import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Central configuration class for the SOC Shadow Box"""
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./soc_shadow_box.db")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Application Settings
    AUTO_RESPONSE_ENABLED = os.getenv("AUTO_RESPONSE_ENABLED", "true").lower() == "true"
    AI_MODEL_PATH = os.getenv("AI_MODEL_PATH", "./backend/app/ai/isolation_forest.pkl")
    WEBSOCKET_ENABLED = os.getenv("WEBSOCKET_ENABLED", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Attack Simulation Settings
    ATTACK_RATE_LIMIT = 100  # Max attacks per minute
    DEFAULT_ATTACK_INTERVAL = 2  # Seconds between automated attacks
    
    # Detection Thresholds
    BRUTE_FORCE_THRESHOLD = 5  # Failed logins in 10 seconds
    DDOS_THRESHOLD = 50  # Requests per second
    FILE_ACTIVITY_THRESHOLD = 20  # File operations in 5 seconds
    
    # Threat Scoring Weights
    RULE_WEIGHT = 0.6
    AI_WEIGHT = 0.4
    
    # Response Actions
    BLOCK_DURATION_HOURS = 1
    MAX_RETRIES = 3

config = Config()