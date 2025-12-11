"""
Statistics Endpoints
Provides statistics and summary endpoints at /api/v1/stats
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get_stats():
    """Get statistics summary"""
    return {"message": "Statistics endpoint"}


@router.get("/summary")
async def get_summary():
    """Get statistics summary"""
    return {"message": "Statistics summary endpoint"}

