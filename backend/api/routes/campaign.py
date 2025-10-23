"""
Campaign generation endpoints with real-time streaming.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import json
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from services.crew_service import MarketingCrew

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
    """

    try:
        # Initialize marketing crew
        crew = MarketingCrew(use_lite=False)

        # Step 1: Philosopher analyzes
        yield f"data: {json.dumps({'step': 1, 'agent': 'philosopher', 'status': 'working', 'message': 'Zeitgeist Philosopher analyzing cultural trends...'})}\n\n"
        await asyncio.sleep(0.5)  # Simulate work

        # TODO: Actually run philosopher analysis
        # philosopher_output = crew.quick_analysis(request.trend_name)

        yield f"data: {json.dumps({'step': 1, 'agent': 'philosopher', 'status': 'complete', 'message': 'Trend analysis complete'})}\n\n"

        # Step 2: Architect creates
        yield f"data: {json.dumps({'step': 2, 'agent': 'architect', 'status': 'working', 'message': 'Cynical Content Architect crafting content...'})}\n\n"
        await asyncio.sleep(0.5)

        yield f"data: {json.dumps({'step': 2, 'agent': 'architect', 'status': 'complete', 'message': 'Initial content created'})}\n\n"

        # Step 3: Optimizer analyzes
        yield f"data: {json.dumps({'step': 3, 'agent': 'optimizer', 'status': 'working', 'message': 'Brutalist Optimizer optimizing for conversion...'})}\n\n"
        await asyncio.sleep(0.5)

        yield f"data: {json.dumps({'step': 3, 'agent': 'optimizer', 'status': 'complete', 'message': 'Optimization recommendations ready'})}\n\n"

        # Step 4: Architect finalizes
        yield f"data: {json.dumps({'step': 4, 'agent': 'architect', 'status': 'working', 'message': 'Creating final optimized content package...'})}\n\n"
        await asyncio.sleep(0.5)

        # TODO: Actually run full pipeline
        # result = crew.analyze_trend(request.trend_name)

        # Mock final output
        final_output = {
            "step": 4,
            "agent": "architect",
            "status": "complete",
            "message": "Campaign generation complete!",
            "data": {
                "narrative": "# Campaign Narrative\n\nStrategic narrative would go here...",
                "blog": "# Blog Post\n\nSEO-optimized blog content...",
                "social_media": {
                    "twitter": ["Tweet 1", "Tweet 2", "Tweet 3"],
                    "instagram": ["IG caption 1", "IG caption 2"],
                    "tiktok": ["TikTok concept 1", "TikTok concept 2"]
                },
                "tshirt_designs": [
                    "Design 1: Visual description",
                    "Design 2: Visual description"
                ]
            }
        }

        yield f"data: {json.dumps(final_output)}\n\n"

    except Exception as e:
        error_msg = {
            "step": 0,
            "agent": "system",
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


@router.get("/status/{campaign_id}")
async def get_campaign_status(campaign_id: str):
    """Get status of a campaign generation job."""
    # TODO: Implement campaign status tracking
    return {
        "campaign_id": campaign_id,
        "status": "completed",
        "progress": 100
    }
