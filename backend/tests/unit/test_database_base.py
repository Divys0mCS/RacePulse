from sqlalchemy.orm import DeclarativeBase

from app.database.base import Base


def test_base_is_declarative_base() -> None:
    assert issubclass(Base, DeclarativeBase)


def test_base_has_metadata() -> None:
    assert Base.metadata is not None