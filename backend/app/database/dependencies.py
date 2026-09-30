from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Provide a database session and always close it afterward."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()