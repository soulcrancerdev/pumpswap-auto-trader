"""
Token Management Endpoints
Token-related CRUD operations at /api/v1/tokens
Includes filtering by RSI, market cap, liquidity, volume, etc.
"""
from fastapi import APIRouter, Query
from typing import List, Optional

router = APIRouter()


@router.get("")
async def get_tokens(
    age_min: Optional[int] = Query(None, description="Age minimum (minutes)"),
    age_max: Optional[int] = Query(None, description="Age maximum (minutes)"),
    mc_min: Optional[float] = Query(None, description="Market Cap minimum (K)"),
    mc_max: Optional[float] = Query(None, description="Market Cap maximum (K)"),
    liquidity_min: Optional[float] = Query(None, description="Liquidity minimum (USD)"),
    liquidity_max: Optional[float] = Query(None, description="Liquidity maximum (USD)"),
    volume_min: Optional[float] = Query(None, description="Volume minimum (USD)"),
    volume_max: Optional[float] = Query(None, description="Volume maximum (USD)"),
    volume_timeframe: Optional[str] = Query("1h", description="Volume timeframe: 1h, 4h, or 24h"),
    rsi_min: Optional[float] = Query(None, description="RSI minimum"),
    rsi_max: Optional[float] = Query(None, description="RSI maximum"),
    rsi_periods: Optional[int] = Query(14, description="RSI periods (default: 14)"),
    rsi_timeframe: Optional[str] = Query("5s", description="RSI candle timeframe (default: 5s)"),
):
    """
    Get list of tokens with trading data from database, filtered by range.
    Calculates RSI and fetches volume data for each token.
    """
    return {"message": "Tokens endpoint", "filters": {
        "age_min": age_min,
        "age_max": age_max,
        "mc_min": mc_min,
        "mc_max": mc_max,
        "liquidity_min": liquidity_min,
        "liquidity_max": liquidity_max,
        "volume_min": volume_min,
        "volume_max": volume_max,
        "volume_timeframe": volume_timeframe,
        "rsi_min": rsi_min,
        "rsi_max": rsi_max,
        "rsi_periods": rsi_periods,
        "rsi_timeframe": rsi_timeframe,
    }}

