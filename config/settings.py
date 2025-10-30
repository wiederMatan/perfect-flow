"""Application configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Prefect Configuration
    prefect_api_url: str = "http://localhost:4200/api"
    prefect_api_key: Optional[str] = None

    # Database Configuration
    postgres_user: str = "prefect"
    postgres_password: str = "prefect"
    postgres_db: str = "prefect"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Application Configuration
    environment: str = "development"
    log_level: str = "INFO"

    @property
    def database_url(self) -> str:
        """Construct database URL from components."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


# Global settings instance
settings = Settings()
