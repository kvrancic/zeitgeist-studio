"""
Configuration management for Zeitgeist Studio backend.
Handles environment variables and application settings.
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"

    # OpenRouter Configuration
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    openrouter_pro_model: str = os.getenv("OPENROUTER_PRO_MODEL", "google/gemini-2.5-pro")
    openrouter_lite_model: str = os.getenv("OPENROUTER_LITE_MODEL", "google/gemini-2.5-flash-lite")

    # Serper API Configuration
    serper_api_key: str = os.getenv("SERPER_API_KEY", "")

    # CORS Settings
    allowed_origins: str = "http://localhost:3000,https://zeitgeist-studio.vercel.app"

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    # File Upload Settings
    max_upload_size_mb: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "5"))
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")
    export_dir: str = os.getenv("EXPORT_DIR", "exports")

    # CrewAI Configuration
    crew_verbose: bool = os.getenv("CREW_VERBOSE", "True").lower() == "true"
    max_rpm: int = int(os.getenv("MAX_RPM", "30"))

    class Config:
        env_file = ".env"
        case_sensitive = False

    def validate(self) -> None:
        """Validate that required configuration is present."""
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is required")
        if not self.serper_api_key:
            raise ValueError("SERPER_API_KEY is required for trend search")

    def get_llm_config(self, use_lite: bool = False) -> dict:
        """Get LLM configuration for CrewAI agents."""
        model = self.openrouter_lite_model if use_lite else self.openrouter_pro_model
        return {
            "model": model,
            "api_key": self.openrouter_api_key,
            "base_url": self.openrouter_base_url
        }


# Global settings instance
settings = Settings()


# Ensure required directories exist
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.export_dir, exist_ok=True)
