from datetime import date

from app.database.connection import SessionLocal
from app.database.models.driver import DriverModel
from app.database.models.lap import LapModel
from app.database.models.race import RaceModel
from app.database.models.session import SessionModel
from app.database.models.team import TeamModel
from app.database.models.track import TrackModel
from app.database.repositories.lap_repository import LapRepository


def test_lap_repository_persists_lap():
    db = SessionLocal()

    try:
        track = TrackModel(
            name="Lap Repository Test Circuit",
            country="Test Country",
            length_km=5.800,
            number_of_corners=17,
        )
        db.add(track)
        db.flush()

        race = RaceModel(
            name="Lap Repository Test Grand Prix",
            season=2026,
            round_number=97,
            track_id=track.track_id,
            race_date=date(2026, 9, 30),
        )
        db.add(race)
        db.flush()

        session = SessionModel(
            race_id=race.race_id,
            session_type="RACE",
        )
        db.add(session)
        db.flush()

        driver = DriverModel(
            name="Integration Test Driver",
            nationality="Test Nationality",
        )
        db.add(driver)
        db.flush()

        team = TeamModel(
            name="Integration Test Team",
            base_country="Test Country",
        )
        db.add(team)
        db.flush()

        repository = LapRepository(db)

        lap = LapModel(
            session_id=session.session_id,
            driver_id=driver.driver_id,
            team_id=team.team_id,
            lap_number=1,
            lap_time_seconds=92.345,
            sector_1_time_seconds=30.120,
            sector_2_time_seconds=31.210,
            sector_3_time_seconds=31.015,
        )

        created_lap = repository.create(lap)
        db.commit()

        assert created_lap.lap_id is not None

        fetched_lap = repository.get_by_id(created_lap.lap_id)

        assert fetched_lap is not None
        assert fetched_lap.session_id == session.session_id
        assert fetched_lap.driver_id == driver.driver_id
        assert fetched_lap.team_id == team.team_id
        assert fetched_lap.lap_number == 1
        assert fetched_lap.lap_time_seconds == 92.345

        fetched_by_composite_key = (
            repository.get_by_session_driver_lap(
                session_id=session.session_id,
                driver_id=driver.driver_id,
                lap_number=1,
            )
        )

        assert fetched_by_composite_key is not None
        assert fetched_by_composite_key.lap_id == created_lap.lap_id

        laps = repository.list_by_session(session.session_id)

        assert len(laps) == 1
        assert laps[0].lap_id == created_lap.lap_id

        repository.delete(fetched_lap)
        db.delete(session)
        db.delete(driver)
        db.delete(team)
        db.delete(race)
        db.delete(track)
        db.commit()

        assert repository.get_by_id(created_lap.lap_id) is None

    finally:
        db.rollback()
        db.close()