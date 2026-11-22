from datetime import date

from app.database.connection import SessionLocal
from app.database.models.race import RaceModel
from app.database.models.track import TrackModel
from app.database.repositories.race_repository import RaceRepository


def test_race_repository_persists_race_with_track():
    db = SessionLocal()
    
    try:
        track = TrackModel(
            name="Race Repository Test Circuit",
            country="Test Country",
            length_km=5.500,
            number_of_corners=16,
        )
        db.add(track)
        db.flush()

        repository = RaceRepository(db)

        race = RaceModel(
            name="Integration Test Grand Prix",
            season=2026,
            round_number=99,
            track_id=track.track_id,
            race_date=date(2026, 9, 30),
        )

        created_race = repository.create(race)
        db.commit()

        assert created_race.race_id is not None
        assert created_race.track_id == track.track_id

        fetched_race = repository.get_by_id(created_race.race_id)

        assert fetched_race is not None
        assert fetched_race.name == "Integration Test Grand Prix"
        assert fetched_race.season == 2026
        assert fetched_race.round_number == 99
        assert fetched_race.track_id == track.track_id
        assert fetched_race.race_date == date(2026, 9, 30)

        # Use limit=200 to ensure we capture the newly created race
        # (database may have many races from previous test runs)
        races = list(repository.list_all(limit=200))

        assert any(
            existing.race_id == created_race.race_id
            for existing in races
        )

        repository.delete(fetched_race)
        db.delete(track)
        db.commit()

        assert repository.get_by_id(created_race.race_id) is None

    finally:
        db.close()