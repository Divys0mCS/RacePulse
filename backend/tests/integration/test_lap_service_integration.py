from datetime import date

from app.database.connection import SessionLocal
from app.database.models.driver import DriverModel
from app.database.models.race import RaceModel
from app.database.models.team import TeamModel
from app.database.models.track import TrackModel
from app.database.services.lap_service import LapService


def test_lap_service_creates_reads_lists_and_deletes_lap():
    db = SessionLocal()

    try:
        track = TrackModel(
            name="Lap Service Integration Test Circuit",
            country="Test Country",
            length_km=5.900,
            number_of_corners=18,
        )
        db.add(track)
        db.flush()

        race = RaceModel(
            name="Lap Service Integration Test",
            season=2026,
            round_number=94,
            track_id=track.track_id,
            race_date=date(2026, 9, 30),
        )
        db.add(race)
        db.flush()

        from app.database.models.session import SessionModel

        session = SessionModel(
            race_id=race.race_id,
            session_type="RACE",
        )
        db.add(session)
        db.flush()

        driver = DriverModel(
            name="Lap Service Integration Driver",
            nationality="Test Nationality",
        )
        db.add(driver)
        db.flush()

        team = TeamModel(
            name="Lap Service Integration Team",
            base_country="Test Country",
        )
        db.add(team)
        db.flush()

        db.commit()

        service = LapService(db)

        created_lap = service.create_lap(
            session_id=session.session_id,
            driver_id=driver.driver_id,
            team_id=team.team_id,
            lap_number=1,
            lap_time_seconds=92.345,
            sector_1_time_seconds=30.120,
            sector_2_time_seconds=31.210,
            sector_3_time_seconds=31.015,
        )

        assert created_lap.lap_id is not None

        fetched_lap = service.get_lap(created_lap.lap_id)

        assert fetched_lap is not None
        assert fetched_lap.session_id == session.session_id
        assert fetched_lap.driver_id == driver.driver_id
        assert fetched_lap.team_id == team.team_id
        assert fetched_lap.lap_number == 1
        assert fetched_lap.lap_time_seconds == 92.345

        fetched_by_composite_key = (
            service.get_lap_by_session_driver_lap(
                session_id=session.session_id,
                driver_id=driver.driver_id,
                lap_number=1,
            )
        )

        assert fetched_by_composite_key is not None
        assert (
            fetched_by_composite_key.lap_id
            == created_lap.lap_id
        )

        session_laps = service.list_laps_by_session(
            session.session_id
        )

        assert len(session_laps) == 1
        assert session_laps[0].lap_id == created_lap.lap_id

        all_laps = service.list_laps()

        assert any(
            lap.lap_id == created_lap.lap_id
            for lap in all_laps
        )

        assert service.delete_lap(created_lap.lap_id) is True
        assert service.get_lap(created_lap.lap_id) is None

        db.delete(session)
        db.delete(driver)
        db.delete(team)
        db.delete(race)
        db.delete(track)
        db.commit()

    finally:
        db.rollback()
        db.close()