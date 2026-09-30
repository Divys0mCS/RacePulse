from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.database.connection import SessionLocal
from app.database.models.driver import DriverModel
from app.database.models.lap import LapModel
from app.database.models.race import RaceModel
from app.database.models.session import SessionModel
from app.database.models.team import TeamModel
from app.database.models.track import TrackModel


def create_lap_dependencies(session):
    track = TrackModel(
        name="Monza",
        country="Italy",
        length_km=5.793,
        number_of_corners=11,
    )
    session.add(track)
    session.commit()
    session.refresh(track)

    race = RaceModel(
        name="Italian Grand Prix",
        season=2026,
        round_number=16,
        track_id=track.track_id,
        race_date=date(2026, 9, 6),
    )
    session.add(race)
    session.commit()
    session.refresh(race)

    race_session = SessionModel(
        race_id=race.race_id,
        session_type="RACE",
    )
    session.add(race_session)
    session.commit()
    session.refresh(race_session)

    driver = DriverModel(
        name="Max Verstappen",
        nationality="Dutch",
    )
    session.add(driver)
    session.commit()
    session.refresh(driver)

    team = TeamModel(
        name="Red Bull Racing",
        base_country="Austria",
    )
    session.add(team)
    session.commit()
    session.refresh(team)

    return track, race, race_session, driver, team


def create_valid_lap(race_session, driver, team) -> LapModel:
    return LapModel(
        session_id=race_session.session_id,
        driver_id=driver.driver_id,
        team_id=team.team_id,
        lap_number=1,
        lap_time_seconds=90.0,
        sector_1_time_seconds=30.0,
        sector_2_time_seconds=35.0,
        sector_3_time_seconds=25.0,
    )


def test_lap_rejects_non_positive_lap_number() -> None:
    session = SessionLocal()

    try:
        track, race, race_session, driver, team = create_lap_dependencies(session)

        lap = create_valid_lap(race_session, driver, team)
        lap.lap_number = 0

        session.add(lap)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

        session.delete(race_session)
        session.delete(race)
        session.delete(track)
        session.delete(driver)
        session.delete(team)
        session.commit()

    finally:
        session.close()


def test_lap_rejects_non_positive_lap_time() -> None:
    session = SessionLocal()

    try:
        track, race, race_session, driver, team = create_lap_dependencies(session)

        lap = create_valid_lap(race_session, driver, team)
        lap.lap_time_seconds = 0

        session.add(lap)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

        session.delete(race_session)
        session.delete(race)
        session.delete(track)
        session.delete(driver)
        session.delete(team)
        session.commit()

    finally:
        session.close()


@pytest.mark.parametrize(
    "field_name",
    [
        "sector_1_time_seconds",
        "sector_2_time_seconds",
        "sector_3_time_seconds",
    ],
)
def test_lap_rejects_non_positive_sector_time(field_name: str) -> None:
    session = SessionLocal()

    try:
        track, race, race_session, driver, team = create_lap_dependencies(session)

        lap = create_valid_lap(race_session, driver, team)
        setattr(lap, field_name, 0)

        session.add(lap)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

        session.delete(race_session)
        session.delete(race)
        session.delete(track)
        session.delete(driver)
        session.delete(team)
        session.commit()

    finally:
        session.close()


def test_lap_rejects_duplicate_session_driver_lap_number() -> None:
    session = SessionLocal()

    try:
        track, race, race_session, driver, team = create_lap_dependencies(session)

        first = create_valid_lap(race_session, driver, team)
        session.add(first)
        session.commit()
        session.refresh(first)

        duplicate = create_valid_lap(race_session, driver, team)
        session.add(duplicate)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

        session.delete(first)
        session.delete(race_session)
        session.delete(race)
        session.delete(track)
        session.delete(driver)
        session.delete(team)
        session.commit()

    finally:
        session.close()


def test_lap_rejects_unknown_session() -> None:
    session = SessionLocal()

    try:
        lap = LapModel(
            session_id=999999,
            driver_id=999999,
            team_id=999999,
            lap_number=1,
            lap_time_seconds=90.0,
            sector_1_time_seconds=30.0,
            sector_2_time_seconds=35.0,
            sector_3_time_seconds=25.0,
        )

        session.add(lap)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    finally:
        session.close()