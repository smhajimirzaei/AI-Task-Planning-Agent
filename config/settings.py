"""Application configuration and settings."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    anthropic_api_key: str

    # Google Calendar
    google_calendar_credentials: str = "credentials.json"
    google_calendar_token: str = "token.json"

    # Microsoft Graph (Outlook)
    microsoft_client_id: Optional[str] = None
    microsoft_client_secret: Optional[str] = None
    microsoft_tenant_id: Optional[str] = None

    # Database
    database_url: str = "sqlite:///./ai_agent.db"

    # Agent Settings
    default_timezone: str = "UTC"
    monitoring_interval_minutes: int = 15
    learning_mode: str = "enabled"

    # AI Model Settings
    model_name: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 4096
    temperature: float = 0.7

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
