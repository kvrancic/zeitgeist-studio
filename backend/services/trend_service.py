"""
Trend discovery service using the Zeitgeist Philosopher agent.
"""

import logging
import re
from typing import List, Dict, Optional
from crewai import Crew, Process
from agents.philosopher import ZeitgeistPhilosopher
from tasks.marketing_tasks import MarketingTasks
from config import settings

logger = logging.getLogger(__name__)


class TrendService:
    """Service for AI-powered trend discovery."""

    def __init__(self, use_lite: bool = False):
        """Initialize trend service with philosopher agent."""
        self.philosopher = ZeitgeistPhilosopher().create(use_lite=use_lite)

    async def discover_trends(
        self,
        company_name: str,
        company_description: str,
        industry: Optional[str] = None
    ) -> Dict:
        """
        Use Philosopher agent to discover relevant trends.

        Returns dict with:
        - trends: List of trend dictionaries
        - search_context: String describing what was analyzed
        """
        try:
            # Validate API keys
            settings.validate()

            # Create custom search context
            search_context = f"""
Company: {company_name}
Description: {company_description}
{f'Industry: {industry}' if industry else ''}

Focus on finding trends that are relevant to this company's market, audience, and brand positioning.
"""

            # Create trend analysis task
            task = MarketingTasks.create_trend_analysis_task(
                agent=self.philosopher,
                topic=search_context
            )

            # Create simple crew with just the philosopher
            crew = Crew(
                agents=[self.philosopher],
                tasks=[task],
                process=Process.sequential,
                verbose=settings.crew_verbose
            )

            # Execute the crew
            logger.info(f"Starting trend discovery for {company_name}...")
            result = crew.kickoff()

            # Parse the result
            trends = self._parse_trends(result)

            logger.info(f"Discovered {len(trends)} trends")

            return {
                "trends": trends,
                "search_context": f"Analyzed current viral trends and cultural movements relevant to {company_name}",
                "raw_analysis": str(result)
            }

        except Exception as e:
            logger.error(f"Trend discovery failed: {e}")
            raise

    def _parse_trends(self, result: str) -> List[Dict]:
        """
        Parse Philosopher's output into structured trend data.

        This is a best-effort parser that extracts trend information
        from the free-form text output.
        """
        trends = []

        # Convert result to string if it's a CrewOutput object
        text = str(result)

        # Try to find trend sections
        # Look for numbered trends or clear patterns
        trend_patterns = [
            r"(?:TREND|Trend)\s*(?:\d+)?[:\-\.]?\s*([^\n]+)\n([^\n]+(?:\n(?!\s*(?:TREND|Trend|\d+\.))[^\n]+)*)",
            r"(?:\d+\.)\s*([^\n]+)\n([^\n]+(?:\n(?!\d+\.)[^\n]+)*)"
        ]

        found_trends = []
        for pattern in trend_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                found_trends.append({
                    "name": match.group(1).strip(),
                    "description": match.group(2).strip()
                })

        # If we found structured trends, use them
        if found_trends:
            for i, trend_data in enumerate(found_trends[:5]):  # Limit to top 5
                trends.append({
                    "trend_name": trend_data["name"][:100],  # Truncate if too long
                    "description": trend_data["description"][:500],
                    "why_its_hot": self._extract_why_hot(text, trend_data["name"]),
                    "relevance_score": max(10 - i, 6),  # Descending scores 10,9,8,7,6
                    "opportunity_window": self._infer_opportunity(text, i),
                    "target_audience": self._extract_audience(text, trend_data["name"])
                })
        else:
            # Fallback: Create a single comprehensive trend from the analysis
            logger.warning("Could not parse structured trends, creating summary trend")
            trends.append({
                "trend_name": "Current Cultural Zeitgeist Analysis",
                "description": text[:500] + "..." if len(text) > 500 else text,
                "why_its_hot": "Based on deep analysis of current psychological and cultural drivers",
                "relevance_score": 8,
                "opportunity_window": "Growing",
                "target_audience": "Culturally-aware consumers seeking authentic expression"
            })

        return trends if trends else self._get_fallback_trends()

    def _extract_why_hot(self, text: str, trend_name: str) -> str:
        """Extract why a trend is hot from the analysis."""
        # Look for psychological analysis near the trend name
        pattern = rf"{re.escape(trend_name)}.{{0,300}}?(psychological|driver|because|truth|need).{{0,200}}"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

        if match:
            snippet = match.group(0).split('.')[-1].strip()
            return snippet[:200] if snippet else "Driven by current cultural and psychological factors"

        return "Reflects current psychological and cultural drivers"

    def _extract_audience(self, text: str, trend_name: str) -> str:
        """Extract target audience from the analysis."""
        # Look for audience mentions
        audience_patterns = [
            r"(?:target|audience|demographic).{0,100}?(Gen Z|Millennials|consumers|users|people aged \d+-\d+)",
            r"(Gen Z|Millennials|young professionals|students)",
        ]

        for pattern in audience_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Trend-conscious consumers"

    def _infer_opportunity(self, text: str, index: int) -> str:
        """Infer opportunity window based on position and text analysis."""
        # Check for urgency keywords
        if re.search(r"peak|now|urgent|immediate|viral|trending", text, re.IGNORECASE):
            return "Peak: Now"
        elif re.search(r"growing|emerging|rising|gaining", text, re.IGNORECASE):
            return "Growing"
        else:
            # First trends are usually more urgent
            return "Peak: Now" if index == 0 else "Growing"

    def _get_fallback_trends(self) -> List[Dict]:
        """Return fallback trends if parsing fails completely."""
        return [{
            "trend_name": "Cultural Analysis in Progress",
            "description": "The Philosopher agent has completed analysis. Check raw output for detailed insights.",
            "why_its_hot": "Analysis contains valuable cultural and psychological insights",
            "relevance_score": 7,
            "opportunity_window": "Growing",
            "target_audience": "General audience"
        }]


# Global service instance
_trend_service: Optional[TrendService] = None


def get_trend_service(use_lite: bool = False) -> TrendService:
    """Get or create the global TrendService instance."""
    global _trend_service
    if _trend_service is None:
        _trend_service = TrendService(use_lite=use_lite)
    return _trend_service
