"""
Zeitgeist Studio - FastAPI Backend
Main application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Zeitgeist Studio API",
    description="AI Marketing Campaign Generator - Backend API",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from api.routes import health, profile, trends, campaign, export

# Include routers
app.include_router(health.router)
app.include_router(profile.router)
app.include_router(trends.router)
app.include_router(campaign.router)
app.include_router(export.router)


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Zeitgeist Studio API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs" if settings.debug else "disabled",
        "endpoints": {
            "health": "/api/health",
            "profile": "/api/profile",
            "trends": "/api/trends",
            "campaign": "/api/campaign",
            "export": "/api/export"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for uncaught errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting Zeitgeist Studio API...")
    try:
        settings.validate()
        logger.info("✓ Configuration validated")
        logger.info(f"✓ CORS origins: {settings.allowed_origins_list}")
        logger.info(f"✓ Upload directory: {settings.upload_dir}")
        logger.info(f"✓ Export directory: {settings.export_dir}")
        logger.info("✓ Zeitgeist Studio API is ready!")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down Zeitgeist Studio API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
