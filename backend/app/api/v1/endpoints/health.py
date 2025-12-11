"""
Health Check Endpoints
Provides health check endpoints at /api/v1/health
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

