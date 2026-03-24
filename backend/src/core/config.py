import logging
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=False)


logger = logging.getLogger(__name__)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    ENV: str = "prod"
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    API_STR: str = "/api"
    PROJECT_NAME: str = "Echo Logic API"
    DEBUG: bool = ENV == "dev"

    # CORS
    CORS_ORIGINS_STR: Optional[str] = ""
    BACKEND_CORS_ORIGINS: Optional[list[str]] = (
        [origin.strip() for origin in CORS_ORIGINS_STR.split(",")]
        if CORS_ORIGINS_STR
        else ["*"]
    )

    # Database
    DB_USER: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASSWORD: str
    DB_FORCE_ROLL_BACK: bool = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        from urllib.parse import quote_plus

        return (
            f"postgresql+asyncpg://{quote_plus(self.DB_USER)}:{quote_plus(self.DB_PASSWORD)}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # LLM
    MODEL_NAME: str = "google_genai:gemini-2.5-flash-lite"
    GOOGLE_API_KEY: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # find query
    PAGE: int = 1
    PAGE_SIZE: int = 10
    ORDERING: str = "-id"


@lru_cache()
def get_config() -> Config:
    return Config()


config = get_config()
