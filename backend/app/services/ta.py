"""
Technical Analysis Utilities
Technical analysis utility functions
Helper functions for calculations
Data processing utilities
"""
import pandas as pd
import pandas_ta as ta


def calculate_rsi(data: pd.DataFrame, periods: int = 14) -> pd.Series:
    """
    Calculate RSI (Relative Strength Index)
    
    Args:
        data: DataFrame with OHLCV data
        periods: Number of periods for RSI calculation (default: 14)
    
    Returns:
        Series with RSI values
    """
    return ta.rsi(data['close'], length=periods)


def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """
    Calculate MACD (Moving Average Convergence Divergence)
    
    Args:
        data: DataFrame with OHLCV data
        fast: Fast EMA period (default: 12)
        slow: Slow EMA period (default: 26)
        signal: Signal line EMA period (default: 9)
    
    Returns:
        Dictionary with MACD line, signal line, and histogram
    """
    macd_data = ta.macd(data['close'], fast=fast, slow=slow, signal=signal)
    return {
        'macd': macd_data[f'MACD_{fast}_{slow}_{signal}'],
        'signal': macd_data[f'MACDs_{fast}_{slow}_{signal}'],
        'histogram': macd_data[f'MACDh_{fast}_{slow}_{signal}'],
    }

