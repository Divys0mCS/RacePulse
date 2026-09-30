import pytest
from sqlalchemy.exc import IntegrityError

from app.database.connection import SessionLocal
from app.database.models.track import TrackModel


def test_database_rejects_non_positive_track_length() -> None:
    with SessionLocal() as session:
        track = TrackModel(
            name="Invalid Length Circuit",
            country="Testland",
            length_km=0,
            number_of_corners=10,
        )

        session.add(track)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()


def test_database_rejects_zero_corners() -> None:
    with SessionLocal() as session:
        track = TrackModel(
            name="Invalid Corner Circuit",
            country="Testland",
            length_km=5.0,
            number_of_corners=0,
        )

        session.add(track)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()