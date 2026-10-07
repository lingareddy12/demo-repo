"""Application-wide configuration, loaded from environment variables."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings object. Import `get_settings()` instead of
    instantiating this class directly, so the values are cached."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "FastAPI Demo Shop"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "sqlite:///./demo_shop.db"

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DEBUG: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance so the .env file is parsed once."""
    return Settings()
