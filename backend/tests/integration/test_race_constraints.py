from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError, ProgrammingError

from app.database.connection import SessionLocal
from app.database.models.race import RaceModel
from app.database.models.track import TrackModel


def create_track(session) -> TrackModel:
    track = TrackModel(
        name="Monza",
        country="Italy",
        length_km=5.793,
        number_of_corners=11,
    )
    session.add(track)
    session.commit()
    session.refresh(track)
    return track


def test_race_rejects_invalid_season() -> None:
    session = SessionLocal()

    try:
        track = create_track(session)

        race = RaceModel(
            name="Invalid Season Race",
            season=1949,
            round_number=1,
            track_id=track.track_id,
            race_date=date(2026, 9, 6),
        )

        session.add(race)

        with pytest.raises((IntegrityError, ProgrammingError)):
            session.commit()

        session.rollback()

        session.delete(track)
        session.commit()

    finally:
        session.close()


def test_race_rejects_invalid_round_number() -> None:
    session = SessionLocal()

    try:
        track = create_track(session)

        race = RaceModel(
            name="Invalid Round Race",
            season=2026,
            round_number=0,
            track_id=track.track_id,
            race_date=date(2026, 9, 6),
        )

        session.add(race)

        with pytest.raises((IntegrityError, ProgrammingError)):
            session.commit()

        session.rollback()

        session.delete(track)
        session.commit()

    finally:
        session.close()


def test_race_rejects_unknown_track() -> None:
    session = SessionLocal()

    try:
        race = RaceModel(
            name="Unknown Track Race",
            season=2026,
            round_number=1,
            track_id=999999,
            race_date=date(2026, 9, 6),
        )

        session.add(race)

        with pytest.raises((IntegrityError, ProgrammingError)):
            session.commit()

        session.rollback()

    finally:
        session.close()