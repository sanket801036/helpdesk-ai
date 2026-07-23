"""Application settings — loaded from environment / .env (pydantic-settings)."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

# Sab helpdesk tables is prefix ke saath banenge (existing ERP tables se collision na ho)
TABLE_PREFIX = "helpdesk_"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # ── App ──
    APP_NAME: str = "Helpdesk AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173"

    # ── Database (PostgreSQL) ──
    # Real values .env se aayenge (git me commit nahi hote).
    # Format: postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DB
    DATABASE_URL: str = (
        "postgresql+asyncpg://helpdesk:helpdesk@localhost:5432/helpdesk"
    )

    # ── JWT ──
    JWT_SECRET_KEY: str = "change_me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── AI (Hugging Face) ──
    AI_PROVIDER: str = "huggingface"
    HF_API_KEY: str = ""
    HF_LLM_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.3"
    HF_EMBED_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    HF_API_BASE: str = "https://api-inference.huggingface.co"
    EMBEDDING_DIM: int = 384  # all-MiniLM-L6-v2

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
