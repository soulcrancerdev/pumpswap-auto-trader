"""
API Router Aggregation
Aggregates all v1 API endpoints
Creates main API router
Includes sub-routers:
- /api/v1/health - Health endpoints
- /api/v1/stats - Statistics endpoints
- /api/v1/tokens - Token endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health, stats, tokens

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(stats.router, prefix="/stats", tags=["stats"])
router.include_router(tokens.router, prefix="/tokens", tags=["tokens"])

