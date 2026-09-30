from datetime import date

from app.database.connection import SessionLocal
from app.database.models.track import TrackModel
from app.database.services.race_service import RaceService


def test_race_service_creates_reads_lists_and_deletes_race():
    db = SessionLocal()

    try:
        track = TrackModel(
            name="Race Service Integration Test Circuit",
            country="Test Country",
            length_km=5.950,
            number_of_corners=19,
        )

        db.add(track)
        db.commit()
        db.refresh(track)

        service = RaceService(db)

        created_race = service.create_race(
            name="Race Service Integration Test",
            season=2026,
            round_number=96,
            track_id=track.track_id,
            race_date=date(2026, 9, 30),
        )

        assert created_race.race_id is not None
        assert created_race.track_id == track.track_id

        fetched_race = service.get_race(created_race.race_id)

        assert fetched_race is not None
        assert fetched_race.name == "Race Service Integration Test"
        assert fetched_race.track_id == track.track_id

        races = service.list_races()

        assert any(
            race.race_id == created_race.race_id
            for race in races
        )

        assert service.delete_race(created_race.race_id) is True
        assert service.get_race(created_race.race_id) is None

        db.delete(track)
        db.commit()

    finally:
        db.rollback()
        db.close()