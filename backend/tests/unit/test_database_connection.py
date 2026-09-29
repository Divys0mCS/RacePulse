from app.config.settings import settings
from app.database.connection import engine, SessionLocal


def test_database_url_is_loaded() -> None:
    assert settings.database_url.startswith("postgresql+psycopg2://")

def test_engine_uses_postgresql_psycopg2() -> None:
    assert engine.url.get_backend_name() == "postgresql"
    assert engine.url.get_driver_name() == "psycopg2"


def test_session_factory_is_configured() -> None:
    session = SessionLocal()

    try:
        assert session.bind is engine
    finally:
        session.close()