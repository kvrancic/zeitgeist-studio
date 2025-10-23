"""
Campaign generation service using the full 3-agent CrewAI pipeline.
Supports streaming progress updates via callbacks.
"""

import logging
import json
from typing import Dict, Callable, Optional
from crewai import Crew, Process
from agents.philosopher import ZeitgeistPhilosopher
from agents.architect import CynicalContentArchitect
from agents.optimizer import BrutalistOptimizer
from tasks.marketing_tasks import MarketingTasks
from config import settings

logger = logging.getLogger(__name__)


class CampaignService:
    """Service for generating marketing campaigns with the 3-agent pipeline."""

    def __init__(self, use_lite: bool = False):
        """Initialize campaign service with all agents."""
        self.philosopher = ZeitgeistPhilosopher().create(use_lite=use_lite)
        self.architect = CynicalContentArchitect().create(use_lite=use_lite)
        self.optimizer = BrutalistOptimizer().create(use_lite=use_lite)

    async def generate_campaign(
        self,
        company_name: str,
        company_description: str,
        brand_voice: str,
        trend_name: str,
        trend_context: str,
        extracted_docs: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Generate complete marketing campaign using 3-agent pipeline.

        Pipeline: Philosopher → Architect → Optimizer → Architect (final)

        Args:
            company_name: Company name
            company_description: Company description
            brand_voice: Brand voice (professional, casual, etc.)
            trend_name: Selected trend name
            trend_context: Context about the trend
            extracted_docs: Optional extracted document context
            progress_callback: Optional callback for progress updates

        Returns:
            Dict with campaign data and metadata
        """
        try:
            # Validate API keys
            settings.validate()

            # Build context
            context = f"""
Company: {company_name}
Description: {company_description}
Brand Voice: {brand_voice}

Trend/Topic: {trend_name}
Trend Context: {trend_context}

{f'Brand Documents Summary: {extracted_docs}' if extracted_docs else ''}

Create a complete marketing campaign that leverages this trend.
"""

            # Create tasks for each agent
            logger.info("Creating agent tasks...")

            # Step 1: Philosopher analyzes the trend
            if progress_callback:
                await progress_callback({
                    "step": 1,
                    "agent": "Zeitgeist Philosopher",
                    "status": "working",
                    "message": "Analyzing cultural drivers and psychological truths..."
                })

            trend_task = MarketingTasks.create_trend_analysis_task(
                agent=self.philosopher,
                topic=context
            )

            # Step 2: Architect creates initial content
            if progress_callback:
                await progress_callback({
                    "step": 2,
                    "agent": "Cynical Content Architect",
                    "status": "working",
                    "message": "Creating viral content and compelling narratives..."
                })

            content_task = MarketingTasks.create_content_generation_task(
                agent=self.architect,
                context=context
            )

            # Step 3: Optimizer enhances SEO and conversion
            if progress_callback:
                await progress_callback({
                    "step": 3,
                    "agent": "Brutalist Optimizer",
                    "status": "working",
                    "message": "Optimizing for SEO and conversion metrics..."
                })

            optimization_task = MarketingTasks.create_optimization_task(
                agent=self.optimizer
            )

            # Step 4: Architect creates final polished version
            if progress_callback:
                await progress_callback({
                    "step": 4,
                    "agent": "Final Content Polish",
                    "status": "working",
                    "message": "Architect creating final optimized campaign..."
                })

            final_task = MarketingTasks.create_final_content_task(
                agent=self.architect,
                context=context
            )

            # Create the crew with sequential process
            logger.info("Assembling marketing crew...")
            crew = Crew(
                agents=[self.philosopher, self.architect, self.optimizer, self.architect],
                tasks=[trend_task, content_task, optimization_task, final_task],
                process=Process.sequential,
                verbose=settings.crew_verbose
            )

            # Execute the crew
            logger.info("Starting campaign generation pipeline...")
            result = crew.kickoff()

            # Mark completion
            if progress_callback:
                await progress_callback({
                    "step": 4,
                    "agent": "Final Content Polish",
                    "status": "complete",
                    "message": "Campaign generation complete!"
                })

            # Parse the result
            campaign_data = self._parse_campaign_result(str(result))

            logger.info("Campaign generation complete")

            return {
                "success": True,
                "campaign": campaign_data,
                "metadata": {
                    "company_name": company_name,
                    "trend_name": trend_name,
                    "brand_voice": brand_voice,
                    "agents_used": 4,
                    "pipeline": "Philosopher → Architect → Optimizer → Architect"
                }
            }

        except Exception as e:
            logger.error(f"Campaign generation failed: {e}")
            if progress_callback:
                await progress_callback({
                    "status": "error",
                    "message": f"Error: {str(e)}"
                })
            raise

    def _parse_campaign_result(self, result: str) -> Dict:
        """
        Parse the final campaign output into structured data.

        This is a best-effort parser that extracts campaign components
        from the Architect's final output.
        """

        # For now, return the raw result
        # In production, this would parse out:
        # - T-shirt designs
        # - Social media posts
        # - Blog post content
        # - SEO metadata

        return {
            "narrative": result[:2000] if len(result) > 2000 else result,  # First 2000 chars
            "full_output": result,
            "blog": {
                "title": "Blog post title will be extracted here",
                "content": "Full blog content...",
                "meta_description": "SEO description..."
            },
            "social_media": {
                "twitter": ["Tweet 1", "Tweet 2", "Tweet 3"],
                "instagram": ["IG caption 1", "IG caption 2"],
                "tiktok": ["TikTok concept 1", "TikTok concept 2"]
            },
            "tshirt_designs": [
                "T-shirt design concept 1",
                "T-shirt design concept 2",
                "T-shirt design concept 3"
            ]
        }


# Global service instance
_campaign_service: Optional[CampaignService] = None


def get_campaign_service(use_lite: bool = False) -> CampaignService:
    """Get or create the global CampaignService instance."""
    global _campaign_service
    if _campaign_service is None or use_lite != getattr(_campaign_service, 'use_lite', False):
        _campaign_service = CampaignService(use_lite=use_lite)
        _campaign_service.use_lite = use_lite
    return _campaign_service
