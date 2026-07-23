from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    """Validated application configuration loaded from environment and ``.env``."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "RouteAI"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = Field(..., min_length=1)
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = Field(..., min_length=1)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., gt=0)
    GEMINI_API_KEY: str = ""
    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"]
    )

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        """Require a synchronous PostgreSQL SQLAlchemy URL."""
        try:
            driver_name = make_url(value).drivername
        except Exception as error:
            raise ValueError("DATABASE_URL must be a valid SQLAlchemy URL") from error

        if driver_name not in {"postgresql", "postgresql+psycopg2"}:
            raise ValueError(
                "DATABASE_URL must use the postgresql or postgresql+psycopg2 driver"
            )
        return value


settings = Settings()
