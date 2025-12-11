"""
FastAPI Application Entry Point
Application initialization and configuration
CORS middleware setup
API router registration (/api prefix)
Lifespan management (startup/shutdown hooks)
Root and health check endpoints
Logging configuration with colored output
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router as api_router
from app.core.config import settings

app = FastAPI(
    title="PumpSwap Auto Trade API",
    description="Automated trading API backend",
    version="0.1.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to PumpSwap Auto Trade API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pumpswap-auto-trade-api"}

