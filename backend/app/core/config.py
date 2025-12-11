"""
Application Settings and Configuration
Pydantic Settings class for configuration management
Loads settings from environment variables
Validates and provides typed configuration access
Settings include: API keys, database URLs, CORS origins, intervals
"""
from pydantic_settings import BaseSettings
from typing import List, Union


class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "PumpSwap Auto Trade API"
    
    # CORS Settings
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./pumpswap.db"
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Trading Settings
    MAX_TRADE_AMOUNT: float = 10000.0
    MIN_TRADE_AMOUNT: float = 10.0
    
    # Birdeye API Settings
    BIRDEYE_API_KEY: str = ""
    BIRDEYE_SLEEP_TIME: float = 0.07
    BIRDEYE_FETCH_LIMIT: int = 100
    BIRDEYE_MAX_WORKERS: int = 15
    
    # Cron Job Settings
    TOKEN_FETCH_INTERVAL_HOURS: int = 1
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

