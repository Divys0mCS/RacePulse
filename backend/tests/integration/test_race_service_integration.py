from datetime import date

from app.database.connection import SessionLocal
from app.database.models.race import RaceModel
from app.database.models.track import TrackModel
from app.database.models.driver import DriverModel
from app.database.models.team import TeamModel
from app.database.repositories.race_repository import RaceRepository
from app.database.repositories.driver_repository import DriverRepository
from app.database.repositories.team_repository import TeamRepository
from app.database.services.race_service import RaceService


def test_race_service_creates_reads_lists_and_deletes_race():
    db = SessionLocal()
    
    try:
        track = TrackModel(
            name="Race Service Test Circuit",
            country="Test Country",
            length_km=5.500,
            number_of_corners=16,
        )
        db.add(track)
        db.commit()

        driver = DriverModel(
            name="Test Driver",
            nationality="Test Nationality",
        )
        db.add(driver)
        db.commit()

        team = TeamModel(
            name="Test Team",
            base_country="Test Country",
        )
        db.add(team)
        db.commit()

        repository = RaceRepository(db)
        service = RaceService(db)

        race = service.create_race(
            name="Integration Test Grand Prix",
            season=2026,
            round_number=99,
            track_id=track.track_id,
            race_date=date(2026, 9, 30),
        )

        fetched_race = repository.get_by_id(race.race_id)

        assert race.race_id is not None
        assert fetched_race is not None
        assert fetched_race.name == "Integration Test Grand Prix"
        assert fetched_race.season == 2026
        assert fetched_race.round_number == 99
        assert fetched_race.track_id == track.track_id
        assert fetched_race.race_date == date(2026, 9, 30)

        # Use limit=200 to ensure we capture the newly created race
        races = list(repository.list_all(limit=200))
        assert any(
            existing.race_id == race.race_id
            for existing in races
        )

        # Update the race
        updated_race = service.update_race(
            race_id=race.race_id,
            name="Updated Race Name",
        )
        assert updated_race.name == "Updated Race Name"

        # Delete the race
        repository.delete(fetched_race)
        db.delete(track)
        db.delete(driver)
        db.delete(team)
        db.commit()

        assert repository.get_by_id(race.race_id) is None

    finally:
        db.close()