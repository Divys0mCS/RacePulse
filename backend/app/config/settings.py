from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    database_url: str
    environment: str = "development"
    debug: bool = True
    cors_origins: str = "http://localhost,http://127.0.0.1"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "change-this-secret"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
print("Settings loaded successfully")
print(f"CORS_ORIGINS: {settings.cors_origins}")
