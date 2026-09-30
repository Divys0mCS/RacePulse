from datetime import date

from app.database.connection import SessionLocal
from app.database.models.race import RaceModel
from app.database.models.track import TrackModel
from app.database.services.session_service import SessionService


def test_session_service_creates_reads_lists_and_deletes_session():
    db = SessionLocal()

    try:
        track = TrackModel(
            name="Session Service Integration Test Circuit",
            country="Test Country",
            length_km=5.900,
            number_of_corners=18,
        )

        db.add(track)
        db.flush()

        race = RaceModel(
            name="Session Service Integration Test",
            season=2026,
            round_number=95,
            track_id=track.track_id,
            race_date=date(2026, 9, 30),
        )

        db.add(race)
        db.commit()
        db.refresh(race)

        service = SessionService(db)

        created_session = service.create_session(
            race_id=race.race_id,
            session_type="QUALIFYING",
        )

        assert created_session.session_id is not None
        assert created_session.race_id == race.race_id
        assert created_session.session_type == "QUALIFYING"

        fetched_session = service.get_session(
            created_session.session_id
        )

        assert fetched_session is not None
        assert fetched_session.race_id == race.race_id
        assert fetched_session.session_type == "QUALIFYING"

        fetched_by_race_and_type = (
            service.get_session_by_race_and_type(
                race_id=race.race_id,
                session_type="QUALIFYING",
            )
        )

        assert fetched_by_race_and_type is not None
        assert (
            fetched_by_race_and_type.session_id
            == created_session.session_id
        )

        sessions = service.list_sessions()

        assert any(
            session.session_id == created_session.session_id
            for session in sessions
        )

        assert service.delete_session(
            created_session.session_id
        ) is True

        assert service.get_session(
            created_session.session_id
        ) is None

        db.delete(race)
        db.delete(track)
        db.commit()

    finally:
        db.rollback()
        db.close()