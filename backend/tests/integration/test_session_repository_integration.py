from datetime import date

from app.database.connection import SessionLocal
from app.database.models.race import RaceModel
from app.database.models.session import SessionModel
from app.database.models.track import TrackModel
from app.database.repositories.session_repository import SessionRepository


def test_session_repository_persists_session():
    db = SessionLocal()

    try:
        track = TrackModel(
            name="Session Repository Test Circuit",
            country="Test Country",
            length_km=5.700,
            number_of_corners=18,
        )

        db.add(track)
        db.flush()

        race = RaceModel(
            name="Session Repository Test Grand Prix",
            season=2026,
            round_number=98,
            track_id=track.track_id,
            race_date=date(2026, 9, 30),
        )

        db.add(race)
        db.flush()

        repository = SessionRepository(db)

        session = SessionModel(
            race_id=race.race_id,
            session_type="QUALIFYING",
        )

        created_session = repository.create(session)
        db.commit()

        assert created_session.session_id is not None
        assert created_session.race_id == race.race_id
        assert created_session.session_type == "QUALIFYING"

        fetched_session = repository.get_by_id(
            created_session.session_id
        )

        assert fetched_session is not None
        assert fetched_session.session_type == "QUALIFYING"

        fetched_by_race_and_type = repository.get_by_race_and_type(
            race.race_id,
            "QUALIFYING",
        )

        assert fetched_by_race_and_type is not None
        assert (
            fetched_by_race_and_type.session_id
            == created_session.session_id
        )

        sessions = repository.list_all()

        assert any(
            existing.session_id == created_session.session_id
            for existing in sessions
        )

        repository.delete(fetched_session)
        db.delete(race)
        db.delete(track)
        db.commit()

        assert repository.get_by_id(created_session.session_id) is None

    finally:
        db.close()