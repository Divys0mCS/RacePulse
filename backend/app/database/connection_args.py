from app.config.settings import settings


def get_connect_args() -> dict:
    """Neon (production) requires SSL; local Postgres and CI do not."""
    if settings.environment == "production":
        return {"ssl_context": True}
    return {}