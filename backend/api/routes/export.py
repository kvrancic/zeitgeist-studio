"""
Export endpoints for PDF and ZIP downloads.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, List
import os
import zipfile
from io import BytesIO
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import settings

router = APIRouter(prefix="/api/export", tags=["export"])


class PDFExportRequest(BaseModel):
    """Request model for PDF export."""
    campaign_id: str
    narrative: str
    company_name: str


class ZIPExportRequest(BaseModel):
    """Request model for ZIP export."""
    campaign_id: str
    narrative: str
    blog: str
    social_media: Dict[str, List[str]]
    tshirt_designs: List[str]
    company_name: str


@router.post("/pdf")
async def export_pdf(request: PDFExportRequest):
    """
    Generate and download campaign narrative as PDF.
    Uses ReportLab for PDF generation.
    """

    try:
        # TODO: Implement actual PDF generation with ReportLab
        # For now, return mock response

        filename = f"campaign_{request.campaign_id}_narrative.pdf"
        filepath = os.path.join(settings.export_dir, filename)

        # Mock: Create a simple text file for now
        with open(filepath, "w") as f:
            f.write(f"Campaign Narrative for {request.company_name}\n\n")
            f.write(request.narrative)

        return FileResponse(
            filepath,
            media_type="application/pdf",
            filename=filename
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")


@router.post("/zip")
async def export_zip(request: ZIPExportRequest):
    """
    Generate and download complete campaign package as ZIP.
    Includes: narrative.pdf, blog_post.md, social_media.txt, tshirt_designs.txt
    """

    try:
        # TODO: Implement actual ZIP generation with all files
        # For now, return mock response

        filename = f"campaign_{request.campaign_id}_complete.zip"
        filepath = os.path.join(settings.export_dir, filename)

        # Create ZIP file
        with zipfile.ZipFile(filepath, 'w') as zipf:
            # Add narrative (mock as text for now)
            zipf.writestr("narrative.txt", request.narrative)

            # Add blog post
            zipf.writestr("blog_post.md", request.blog)

            # Add social media content
            social_content = ""
            for platform, posts in request.social_media.items():
                social_content += f"\n## {platform.upper()}\n\n"
                for i, post in enumerate(posts, 1):
                    social_content += f"{i}. {post}\n\n"
            zipf.writestr("social_media.txt", social_content)

            # Add t-shirt designs
            designs_content = "\n\n".join(request.tshirt_designs)
            zipf.writestr("tshirt_designs.txt", designs_content)

        return FileResponse(
            filepath,
            media_type="application/zip",
            filename=filename
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ZIP export failed: {str(e)}")


@router.delete("/cleanup/{campaign_id}")
async def cleanup_exports(campaign_id: str):
    """Clean up exported files for a campaign."""
    try:
        # Remove files from export directory
        for filename in os.listdir(settings.export_dir):
            if campaign_id in filename:
                os.remove(os.path.join(settings.export_dir, filename))

        return {"success": True, "message": f"Cleaned up exports for campaign {campaign_id}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")
