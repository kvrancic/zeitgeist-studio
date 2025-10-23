"""
Company profile management endpoints.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
import os
import logging

from services.document_service import get_document_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/profile", tags=["profile"])


class BrandVoice(str, Enum):
    """Brand voice options."""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    EDGY = "edgy"
    INSPIRATIONAL = "inspirational"
    HUMOROUS = "humorous"
    CUSTOM = "custom"


class CompanyProfile(BaseModel):
    """Company profile data model."""
    company_name: str = Field(..., min_length=3, max_length=100)
    company_description: str = Field(..., min_length=100, max_length=2000)
    brand_voice: BrandVoice
    brand_voice_custom: Optional[str] = Field(None, max_length=500)
    extracted_context: Optional[str] = None


class ProfileResponse(BaseModel):
    """Response model for profile creation."""
    success: bool
    message: str
    profile: CompanyProfile
    files_processed: Optional[List[str]] = None


@router.post("/create", response_model=ProfileResponse)
async def create_profile(
    company_name: str = Form(...),
    company_description: str = Form(...),
    brand_voice: BrandVoice = Form(...),
    brand_voice_custom: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None)
):
    """
    Create or update company profile.
    Accepts company info and optional document uploads.
    """

    # Validate inputs
    if len(company_name) < 3 or len(company_name) > 100:
        raise HTTPException(status_code=400, detail="Company name must be 3-100 characters")

    if len(company_description) < 100 or len(company_description) > 2000:
        raise HTTPException(status_code=400, detail="Description must be 100-2000 characters")

    # Process uploaded files with document extraction
    extracted_context = ""
    processed_files = []

    if files:
        doc_service = get_document_service()
        extracted_texts = []

        for file in files:
            if file.size > 5 * 1024 * 1024:  # 5MB limit
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} exceeds 5MB limit"
                )

            # Check file type
            allowed_extensions = ['.pdf', '.docx', '.txt']
            file_ext = os.path.splitext(file.filename)[1].lower()
            if file_ext not in allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type {file_ext} not supported. Allowed: {', '.join(allowed_extensions)}"
                )

            # Extract text from document
            try:
                content = await file.read()
                text = await doc_service.extract_text(content, file.filename)

                if text:
                    extracted_texts.append(text)
                    processed_files.append(file.filename)
                    logger.info(f"Extracted {len(text)} chars from {file.filename}")
                else:
                    logger.warning(f"No text extracted from {file.filename}")

            except Exception as e:
                logger.error(f"Error processing {file.filename}: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to process {file.filename}: {str(e)}"
                )

        # Summarize all extracted texts into brand context
        if extracted_texts:
            try:
                extracted_context = await doc_service.summarize_for_brand_context(
                    extracted_texts,
                    company_name,
                    max_tokens=3000
                )
                logger.info(f"Summarized {len(extracted_texts)} documents into {len(extracted_context or '')} chars")
            except Exception as e:
                logger.error(f"Error summarizing documents: {e}")
                # Continue without summary rather than failing
                extracted_context = None

    # Create profile object
    profile = CompanyProfile(
        company_name=company_name,
        company_description=company_description,
        brand_voice=brand_voice,
        brand_voice_custom=brand_voice_custom if brand_voice == BrandVoice.CUSTOM else None,
        extracted_context=extracted_context if extracted_context else None
    )

    return ProfileResponse(
        success=True,
        message="Profile created successfully",
        profile=profile,
        files_processed=processed_files if processed_files else None
    )


@router.get("/validate")
async def validate_profile(company_name: str):
    """Validate that a company profile exists (for frontend checks)."""
    # For MVP, this is a simple check
    # In production, this would check localStorage or database
    return {
        "valid": True if company_name else False,
        "company_name": company_name
    }
