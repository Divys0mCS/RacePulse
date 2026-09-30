from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.database.connection import SessionLocal
from app.database.models.race import RaceModel
from app.database.models.session import SessionModel
from app.database.models.track import TrackModel


def create_race(session) -> RaceModel:
    track = TrackModel(
        name="Monaco",
        country="Monaco",
        length_km=3.337,
        number_of_corners=19,
    )
    session.add(track)
    session.commit()
    session.refresh(track)

    race = RaceModel(
        name="Monaco Grand Prix",
        season=2026,
        round_number=8,
        track_id=track.track_id,
        race_date=date(2026, 5, 24),
    )
    session.add(race)
    session.commit()
    session.refresh(race)

    return race


def test_session_rejects_invalid_session_type() -> None:
    session = SessionLocal()

    try:
        race = create_race(session)

        invalid_session = SessionModel(
            race_id=race.race_id,
            session_type="PRACTICE",
        )

        session.add(invalid_session)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

        session.delete(race.track)
        session.delete(race)
        session.commit()

    finally:
        session.close()


def test_session_rejects_duplicate_session_type_for_same_race() -> None:
    session = SessionLocal()

    try:
        race = create_race(session)

        first = SessionModel(
            race_id=race.race_id,
            session_type="QUALIFYING",
        )

        second = SessionModel(
            race_id=race.race_id,
            session_type="QUALIFYING",
        )

        session.add(first)
        session.commit()

        session.add(second)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

        session.delete(first)
        session.delete(race.track)
        session.delete(race)
        session.commit()

    finally:
        session.close()


def test_session_rejects_unknown_race() -> None:
    session = SessionLocal()

    try:
        invalid_session = SessionModel(
            race_id=999999,
            session_type="FP1",
        )

        session.add(invalid_session)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    finally:
        session.close()