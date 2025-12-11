"""
Token Data Models
SQLAlchemy ORM models for tokens
Defines database table schemas
Relationships and constraints
"""
from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_address = Column(String, unique=True, index=True)
    token_name = Column(String)
    symbol = Column(String)
    market_cap = Column(Float)
    liquidity = Column(Float)
    volume_1h_usd = Column(Float)
    volume_4h_usd = Column(Float)
    volume_24h_usd = Column(Float)
    age_days = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

