"""
Document extraction and summarization service.
Handles PDF, DOCX, and TXT file processing with intelligent summarization.
"""

import io
import logging
from typing import Optional
from PyPDF2 import PdfReader
from docx import Document
from openai import OpenAI
from config import settings

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for extracting and summarizing document content."""

    def __init__(self):
        """Initialize the document service with OpenRouter client."""
        self.client = OpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
        )
        self.model = settings.openrouter_pro_model  # Use pro model for summarization

    async def extract_text(self, file_content: bytes, filename: str) -> str:
        """
        Extract text from uploaded file based on file type.

        Args:
            file_content: Raw file bytes
            filename: Original filename to determine type

        Returns:
            Extracted text content
        """
        file_lower = filename.lower()

        try:
            if file_lower.endswith('.pdf'):
                return self._extract_from_pdf(file_content)
            elif file_lower.endswith('.docx'):
                return self._extract_from_docx(file_content)
            elif file_lower.endswith('.txt'):
                return self._extract_from_txt(file_content)
            else:
                logger.warning(f"Unsupported file type: {filename}")
                return ""
        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {e}")
            return ""

    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file."""
        try:
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)

            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return ""

    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX file."""
        try:
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)

            text_parts = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)

            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            return ""

    def _extract_from_txt(self, file_content: bytes) -> str:
        """Extract text from TXT file."""
        try:
            return file_content.decode('utf-8', errors='ignore')
        except Exception as e:
            logger.error(f"TXT extraction error: {e}")
            return ""

    async def summarize_for_brand_context(
        self,
        extracted_texts: list[str],
        company_name: str,
        max_tokens: int = 3000
    ) -> Optional[str]:
        """
        Summarize extracted document texts into brand context.

        Args:
            extracted_texts: List of extracted text from documents
            company_name: Name of the company for context
            max_tokens: Target token count for summary (~3000 = ~12000 chars)

        Returns:
            Summarized brand context or None if summarization fails
        """
        if not extracted_texts:
            return None

        # Combine all extracted texts
        combined_text = "\n\n---\n\n".join(extracted_texts)

        # If text is already short enough, return as-is
        if len(combined_text) < max_tokens * 4:  # Rough estimate: 1 token ≈ 4 chars
            return combined_text

        # Summarize using LLM
        try:
            logger.info(f"Summarizing {len(combined_text)} chars of documents for {company_name}")

            system_prompt = """You are an expert brand analyst. Extract and summarize key information about a company's:
- Brand identity and values
- Product/service offerings
- Target audience and positioning
- Voice and tone guidelines
- Marketing themes and messaging
- Company history and achievements
- Unique selling propositions

Focus on information that would be useful for creating marketing campaigns."""

            user_prompt = f"""Company Name: {company_name}

Documents:
{combined_text}

Provide a comprehensive summary (target: ~3000 tokens / ~12000 characters) that captures the essential brand context and marketing-relevant information from these documents."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=3500,  # Slightly more than target to ensure full summary
                temperature=0.3,  # Lower temperature for more focused extraction
            )

            summary = response.choices[0].message.content
            logger.info(f"Successfully summarized to {len(summary)} chars")

            return summary

        except Exception as e:
            logger.error(f"Summarization error: {e}")
            # Fallback: truncate to target length
            fallback_length = max_tokens * 4
            logger.warning(f"Falling back to truncation at {fallback_length} chars")
            return combined_text[:fallback_length] + "\n\n[...truncated for length]"


# Global instance
_document_service: Optional[DocumentService] = None


def get_document_service() -> DocumentService:
    """Get or create the global DocumentService instance."""
    global _document_service
    if _document_service is None:
        _document_service = DocumentService()
    return _document_service
