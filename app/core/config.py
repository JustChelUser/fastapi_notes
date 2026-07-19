from functools import lru_cache
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

core_dir = Path(__file__).parent
ENV_FILE_PATH = core_dir.parent / ".env"


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    cors_allowed_origins: list[str]
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


@lru_cache
def get_settings() -> Settings:
    return Settings()
