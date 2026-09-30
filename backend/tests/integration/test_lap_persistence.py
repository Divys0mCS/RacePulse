from datetime import date

from app.database.connection import SessionLocal
from app.database.models.driver import DriverModel
from app.database.models.lap import LapModel
from app.database.models.race import RaceModel
from app.database.models.session import SessionModel
from app.database.models.team import TeamModel
from app.database.models.track import TrackModel


def test_lap_can_be_inserted_and_read_back() -> None:
    db = SessionLocal()

    try:
        track = TrackModel(
            name="Silverstone",
            country="United Kingdom",
            length_km=5.891,
            number_of_corners=18,
        )
        db.add(track)
        db.commit()
        db.refresh(track)

        race = RaceModel(
            name="British Grand Prix",
            season=2026,
            round_number=12,
            track_id=track.track_id,
            race_date=date(2026, 7, 5),
        )
        db.add(race)
        db.commit()
        db.refresh(race)

        session_model = SessionModel(
            race_id=race.race_id,
            session_type="RACE",
        )
        db.add(session_model)
        db.commit()
        db.refresh(session_model)

        driver = DriverModel(
            name="Max Verstappen",
            nationality="Dutch",
        )
        db.add(driver)
        db.commit()
        db.refresh(driver)

        team = TeamModel(
            name="Red Bull Racing",
            base_country="Austria",
        )
        db.add(team)
        db.commit()
        db.refresh(team)

        lap = LapModel(
            session_id=session_model.session_id,
            driver_id=driver.driver_id,
            team_id=team.team_id,
            lap_number=42,
            lap_time_seconds=88.421,
            sector_1_time_seconds=28.104,
            sector_2_time_seconds=34.512,
            sector_3_time_seconds=25.805,
        )

        db.add(lap)
        db.commit()
        db.refresh(lap)

        assert lap.lap_id is not None

        saved_lap = db.get(LapModel, lap.lap_id)

        assert saved_lap is not None
        assert saved_lap.session_id == session_model.session_id
        assert saved_lap.driver_id == driver.driver_id
        assert saved_lap.team_id == team.team_id
        assert saved_lap.lap_number == 42
        assert saved_lap.lap_time_seconds == 88.421
        assert saved_lap.sector_1_time_seconds == 28.104
        assert saved_lap.sector_2_time_seconds == 34.512
        assert saved_lap.sector_3_time_seconds == 25.805

        assert saved_lap.session is not None
        assert saved_lap.session.session_id == session_model.session_id
        assert saved_lap.session.session_type == "RACE"

        assert saved_lap.driver is not None
        assert saved_lap.driver.driver_id == driver.driver_id
        assert saved_lap.driver.name == "Max Verstappen"

        assert saved_lap.team is not None
        assert saved_lap.team.team_id == team.team_id
        assert saved_lap.team.name == "Red Bull Racing"

        saved_session = db.get(SessionModel, session_model.session_id)
        assert saved_session is not None
        assert len(saved_session.laps) == 1
        assert saved_session.laps[0].lap_id == lap.lap_id

        saved_driver = db.get(DriverModel, driver.driver_id)
        assert saved_driver is not None
        assert len(saved_driver.laps) == 1
        assert saved_driver.laps[0].lap_id == lap.lap_id

        saved_team = db.get(TeamModel, team.team_id)
        assert saved_team is not None
        assert len(saved_team.laps) == 1
        assert saved_team.laps[0].lap_id == lap.lap_id

        db.delete(lap)
        db.delete(session_model)
        db.delete(race)
        db.delete(track)
        db.delete(driver)
        db.delete(team)
        db.commit()

    finally:
        db.close()