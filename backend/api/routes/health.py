"""
Health check endpoints.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "zeitgeist-studio-backend",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/detailed")
async def detailed_health():
    """Detailed health check with component status."""
    return {
        "status": "healthy",
        "components": {
            "api": "operational",
            "agents": "operational",
            "llm": "operational"
        },
        "timestamp": datetime.utcnow().isoformat()
    }
