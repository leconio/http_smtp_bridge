"""
Configuration management using pydantic-settings
"""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # Application settings
    app_name: str = "SMTP Bridge"
    debug: bool = False

    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000
    workers: int = 4

    # SMTP settings
    smtp_host: str = Field(..., description="SMTP server hostname")
    smtp_port: int = Field(587, description="SMTP server port")
    smtp_username: Optional[str] = Field(None, description="SMTP username")
    smtp_password: Optional[str] = Field(None, description="SMTP password")
    smtp_use_tls: bool = Field(True, description="Use TLS for SMTP")
    smtp_timeout: int = Field(30, description="SMTP connection timeout in seconds")

    # Security settings
    api_key: Optional[str] = Field(None, description="API key for authentication")
    allowed_origins: list[str] = Field(default_factory=lambda: ["*"], description="CORS allowed origins")

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds

    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()
