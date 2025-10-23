"""
Trend identification endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from services.crew_service import MarketingCrew

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
    """

    try:
        # Initialize marketing crew with pro model
        crew = MarketingCrew(use_lite=False)

        # TODO: Implement actual trend search with Philosopher
        # For now, return mock data

        mock_trends = [
            Trend(
                trend_name="AI-Powered Personalization",
                description="Consumers expect hyper-personalized experiences powered by AI across all touchpoints.",
                why_its_hot="Desire for unique, tailored experiences that feel human despite automation.",
                relevance_score=9,
                opportunity_window=OpportunityWindow.PEAK_NOW,
                target_audience="Tech-savvy consumers aged 25-45"
            ),
            Trend(
                trend_name="Nostalgia for Analog",
                description="Gen Z discovering film photography, vinyl records, and 'slow' experiences.",
                why_its_hot="Rebellion against algorithmic feeds and infinite digital scroll.",
                relevance_score=8,
                opportunity_window=OpportunityWindow.GROWING,
                target_audience="Gen Z and young millennials"
            ),
            Trend(
                trend_name="Sustainability as Status",
                description="Eco-friendly choices becoming the new luxury signaling.",
                why_its_hot="Social pressure and genuine concern merge into purchasing behavior.",
                relevance_score=7,
                opportunity_window=OpportunityWindow.PEAK_NOW,
                target_audience="Affluent consumers, all ages"
            )
        ]

        return TrendSearchResponse(
            success=True,
            trends=mock_trends[:5],  # Return top 5
            search_context=f"Analyzed trends for {request.company_name} in context of their market"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend search failed: {str(e)}")


@router.post("/manual", response_model=ManualTrendResponse)
async def submit_manual_trend(request: ManualTrendRequest):
    """
    User submits a manual topic/trend.
    Philosopher agent provides quick analysis and enrichment.
    """

    try:
        # Initialize marketing crew
        crew = MarketingCrew(use_lite=False)

        # TODO: Implement quick philosopher analysis
        # For now, return enriched trend

        enriched_trend = Trend(
            trend_name=request.topic,
            description=f"Analysis of {request.topic} and its market relevance.",
            why_its_hot="Based on current cultural and psychological drivers.",
            relevance_score=7,
            opportunity_window=OpportunityWindow.GROWING,
            target_audience="To be determined based on campaign development"
        )

        return ManualTrendResponse(
            success=True,
            trend=enriched_trend,
            analysis=f"Quick analysis completed for: {request.topic}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")
