from app.config.settings import settings
from app.database.connection import engine


def test_database_url_is_loaded() -> None:
    assert settings.database_url.startswith("postgresql+pg8000://")


def test_engine_uses_postgresql_pg8000() -> None:
    assert engine.url.get_backend_name() == "postgresql"
    assert engine.url.get_driver_name() == "pg8000"