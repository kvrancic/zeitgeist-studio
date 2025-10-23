"""
Trend identification endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import sys
import os
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from services.trend_service import get_trend_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/trends", tags=["trends"])


class OpportunityWindow(str, Enum):
    """Opportunity window for trend."""
    PEAK_NOW = "Peak: Now"
    GROWING = "Growing"
    EARLY = "Early"


class Trend(BaseModel):
    """Trend data model."""
    trend_name: str
    description: str
    why_its_hot: str
    relevance_score: int = Field(..., ge=1, le=10)
    opportunity_window: OpportunityWindow
    target_audience: Optional[str] = None


class TrendSearchRequest(BaseModel):
    """Request model for AI trend search."""
    company_name: str
    company_description: str
    industry: Optional[str] = None


class TrendSearchResponse(BaseModel):
    """Response model for trend search."""
    success: bool
    trends: List[Trend]
    search_context: str


class ManualTrendRequest(BaseModel):
    """Request model for manual trend input."""
    topic: str = Field(..., min_length=5, max_length=200)
    company_context: Optional[str] = None


class ManualTrendResponse(BaseModel):
    """Response model for manual trend."""
    success: bool
    trend: Trend
    analysis: str


@router.post("/search", response_model=TrendSearchResponse)
async def search_trends(request: TrendSearchRequest):
    """
    AI-powered trend discovery using Zeitgeist Philosopher agent.
    Searches web for trending topics relevant to the company.

    Note: Requires OPENROUTER_API_KEY and SERPER_API_KEY in environment.
    """

    try:
        logger.info(f"Starting trend search for {request.company_name}")

        # Get trend service (use pro model for better analysis)
        trend_service = get_trend_service(use_lite=False)

        # Discover trends using Philosopher agent
        result = await trend_service.discover_trends(
            company_name=request.company_name,
            company_description=request.company_description,
            industry=request.industry
        )

        # Convert parsed trends to Pydantic models
        trends = [
            Trend(
                trend_name=t["trend_name"],
                description=t["description"],
                why_its_hot=t["why_its_hot"],
                relevance_score=t["relevance_score"],
                opportunity_window=OpportunityWindow(t["opportunity_window"]),
                target_audience=t.get("target_audience")
            )
            for t in result["trends"]
        ]

        logger.info(f"Successfully discovered {len(trends)} trends")

        return TrendSearchResponse(
            success=True,
            trends=trends,
            search_context=result["search_context"]
        )

    except ValueError as e:
        # API key missing or validation error
        logger.error(f"Configuration error: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Service not configured: {str(e)}. Please set OPENROUTER_API_KEY and SERPER_API_KEY."
        )
    except Exception as e:
        logger.error(f"Trend search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Trend search failed: {str(e)}")


@router.post("/manual", response_model=ManualTrendResponse)
async def submit_manual_trend(request: ManualTrendRequest):
    """
    User submits a manual topic/trend.
    Philosopher agent provides quick analysis and enrichment.

    Note: Uses lite model for faster response. Requires OPENROUTER_API_KEY and SERPER_API_KEY.
    """

    try:
        logger.info(f"Analyzing manual trend: {request.topic}")

        # Get trend service (use lite model for quick analysis)
        trend_service = get_trend_service(use_lite=True)

        # Build context if provided
        search_context = f"""
Topic/Trend: {request.topic}
{f'Company Context: {request.company_context}' if request.company_context else ''}

Provide a quick analysis of this trend including psychological drivers, target audience, and marketing potential.
"""

        # Discover trend analysis using Philosopher
        result = await trend_service.discover_trends(
            company_name="User Input",
            company_description=search_context,
            industry=None
        )

        # Take the first trend or create one from the analysis
        if result["trends"]:
            trend_data = result["trends"][0]
            # Override name with user's input
            trend_data["trend_name"] = request.topic

            enriched_trend = Trend(
                trend_name=trend_data["trend_name"],
                description=trend_data["description"],
                why_its_hot=trend_data["why_its_hot"],
                relevance_score=trend_data["relevance_score"],
                opportunity_window=OpportunityWindow(trend_data["opportunity_window"]),
                target_audience=trend_data.get("target_audience")
            )
        else:
            # Fallback if no trends parsed
            enriched_trend = Trend(
                trend_name=request.topic,
                description="Philosopher analysis completed. See full analysis for details.",
                why_its_hot="Based on cultural and psychological analysis",
                relevance_score=7,
                opportunity_window=OpportunityWindow.GROWING,
                target_audience="To be refined during campaign creation"
            )

        logger.info(f"Successfully analyzed manual trend: {request.topic}")

        return ManualTrendResponse(
            success=True,
            trend=enriched_trend,
            analysis=result.get("raw_analysis", result["search_context"])[:1000]  # Truncate for response
        )

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Service not configured: {str(e)}. Please set OPENROUTER_API_KEY and SERPER_API_KEY."
        )
    except Exception as e:
        logger.error(f"Manual trend analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")
