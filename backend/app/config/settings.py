from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    database_url: str
    environment: str = "development"
    debug: bool = True
    cors_origins: str = "http://localhost,http://127.0.0.1"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str
    api_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def model_validate(self, *args, **kwargs):
        """Validate that SECRET_KEY is set in production."""
        instance = super().model_validate(*args, **kwargs)
        if instance.environment == "production" and not instance.secret_key:
            raise ValueError(
                "SECRET_KEY must be set when ENVIRONMENT=production. "
                "Generate with: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        return instance


settings = Settings()
print("Settings loaded successfully")
print(f"CORS_ORIGINS: {settings.cors_origins}")
print(f"API_PORT: {settings.api_port}")