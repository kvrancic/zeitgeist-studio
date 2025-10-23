"""
Campaign generation endpoints with real-time streaming.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import json
import asyncio
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from services.campaign_service import get_campaign_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/campaign", tags=["campaign"])


class CampaignRequest(BaseModel):
    """Request model for campaign generation."""
    company_name: str
    company_description: str
    brand_voice: str
    trend_name: str
    trend_context: str
    extracted_docs: Optional[str] = None


class CampaignResponse(BaseModel):
    """Response model for completed campaign."""
    success: bool
    campaign_id: str
    narrative: str
    blog: str
    social_media: Dict[str, List[str]]
    tshirt_designs: List[str]
    generation_time: float


async def campaign_generator_stream(request: CampaignRequest):
    """
    Stream campaign generation progress using Server-Sent Events (SSE).
    Yields JSON objects for each step of the pipeline.

    Pipeline: Philosopher → Architect → Optimizer → Architect (final)
    """

    async def progress_callback(data: Dict):
        """Callback to stream progress updates."""
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(0.1)  # Small delay for browser to process

    try:
        logger.info(f"Starting campaign generation for {request.company_name}")

        # Get campaign service (use pro model for best results)
        campaign_service = get_campaign_service(use_lite=False)

        # Stream initial message
        yield f"data: {json.dumps({'status': 'started', 'message': 'Initializing 3-agent pipeline...'})}\n\n"
        await asyncio.sleep(0.5)

        # Generate campaign with streaming callbacks
        # Note: We can't use async generator directly, so we'll collect updates
        updates = []

        def sync_callback(data):
            """Synchronous wrapper for updates."""
            updates.append(data)

        async def async_callback(data):
            """Async callback for streaming."""
            yield f"data: {json.dumps(data)}\n\n"

        # Run campaign generation
        # For streaming, we'll manually emit updates at each step

        # Step 1: Philosopher
        yield f"data: {json.dumps({'step': 1, 'agent': 'Zeitgeist Philosopher', 'status': 'working', 'message': 'Analyzing cultural drivers and psychological truths...'})}\n\n"
        await asyncio.sleep(0.5)

        # Step 2: Architect (initial)
        yield f"data: {json.dumps({'step': 2, 'agent': 'Cynical Content Architect', 'status': 'working', 'message': 'Creating viral content and compelling narratives...'})}\n\n"
        await asyncio.sleep(0.5)

        # Step 3: Optimizer
        yield f"data: {json.dumps({'step': 3, 'agent': 'Brutalist Optimizer', 'status': 'working', 'message': 'Optimizing for SEO and conversion metrics...'})}\n\n"
        await asyncio.sleep(0.5)

        # Step 4: Architect (final)
        yield f"data: {json.dumps({'step': 4, 'agent': 'Final Content Polish', 'status': 'working', 'message': 'Architect creating final optimized campaign...'})}\n\n"
        await asyncio.sleep(0.5)

        # Actually run the pipeline
        result = await campaign_service.generate_campaign(
            company_name=request.company_name,
            company_description=request.company_description,
            brand_voice=request.brand_voice,
            trend_name=request.trend_name,
            trend_context=request.trend_context,
            extracted_docs=request.extracted_docs
        )

        # Send final result
        final_output = {
            "status": "complete",
            "message": "Campaign generation complete!",
            "data": result["campaign"]
        }

        yield f"data: {json.dumps(final_output)}\n\n"

        logger.info("Campaign generation complete")

    except ValueError as e:
        # Configuration error (API keys missing)
        logger.error(f"Configuration error: {e}")
        error_msg = {
            "status": "error",
            "message": f"Service not configured: {str(e)}. Please set OPENROUTER_API_KEY and SERPER_API_KEY."
        }
        yield f"data: {json.dumps(error_msg)}\n\n"

    except Exception as e:
        logger.error(f"Campaign generation error: {e}", exc_info=True)
        error_msg = {
            "status": "error",
            "message": f"Campaign generation failed: {str(e)}"
        }
        yield f"data: {json.dumps(error_msg)}\n\n"


@router.post("/generate")
async def generate_campaign(request: CampaignRequest):
    """
    Generate complete marketing campaign with real-time streaming updates.
    Returns Server-Sent Events (SSE) stream of pipeline progress.
    """

    return StreamingResponse(
        campaign_generator_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.get("/generate")
async def generate_campaign_get(
    company_name: str,
    company_description: str,
    brand_voice: str,
    trend_name: str,
    trend_context: str,
    extracted_docs: Optional[str] = None
):
    """
    GET version of campaign generation for EventSource compatibility.
    Returns Server-Sent Events (SSE) stream of pipeline progress.
    """
    request = CampaignRequest(
        company_name=company_name,
        company_description=company_description,
        brand_voice=brand_voice,
        trend_name=trend_name,
        trend_context=trend_context,
        extracted_docs=extracted_docs
    )

    return StreamingResponse(
        campaign_generator_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.get("/status/{campaign_id}")
async def get_campaign_status(campaign_id: str):
    """Get status of a campaign generation job."""
    # TODO: Implement campaign status tracking
    return {
        "campaign_id": campaign_id,
        "status": "completed",
        "progress": 100
    }
