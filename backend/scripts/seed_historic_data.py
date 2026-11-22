"""
Seed a limited subset of historic lap data for the free-tier database.

This script loads a small number of sessions and laps to keep the
free-tier database small while still providing useful test data.

Run with: python -m scripts.seed_historic_data
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings
from app.database.base import Base
from app.database.models import RaceModel, SessionModel, DriverModel, TeamModel, LapModel, TrackModel
from app.database.repositories import (
    RaceRepository,
    SessionRepository,
    DriverRepository,
    TeamRepository,
    LapRepository,
    TrackRepository,
)


def get_engine():
    """Create database engine from settings."""
    return create_engine(settings.database_url, pool_pre_ping=True)


def create_tables(engine):
    """Create all tables if they don't exist."""
    Base.metadata.create_all(engine)


def seed_data(session):
    """Seed a limited subset of historic data."""

    # Create a track if it doesn't exist
    track_repo = TrackRepository(session)
    track = track_repo.get_by_name("Monaco Grand Prix Circuit")
    if track is None:
        track = TrackModel(
            name="Monaco Grand Prix Circuit",
            country="Monaco",
            length_km=3.337,
            number_of_corners=19,
        )
        session.add(track)
        session.flush()

    # Create a race if it doesn't exist
    race_repo = RaceRepository(session)
    race = race_repo.get_by_name("Monaco Grand Prix 2024")
    if race is None:
        race = RaceModel(
            name="Monaco Grand Prix 2024",
            season=2024,
            round_number=1,
            track_id=track.track_id,
            race_date="2024-05-26",
        )
        session.add(race)
        session.flush()

    # Create sessions if they don't exist
    session_repo = SessionRepository(session)
    sessions_data = [
        {"session_type": "FP1", "race_id": race.race_id},
        {"session_type": "FP2", "race_id": race.race_id},
        {"session_type": "FP3", "race_id": race.race_id},
        {"session_type": "QUALIFYING", "race_id": race.race_id},
        {"session_type": "RACE", "race_id": race.race_id},
    ]

    for sd in sessions_data:
        existing = session_repo.get_by_race_and_type(sd["race_id"], sd["session_type"])
        if existing is None:
            session_model = SessionModel(
                session_type=sd["session_type"],
                race_id=sd["race_id"],
            )
            session.add(session_model)
            session.flush()

    # Create drivers if they don't exist
    driver_repo = DriverRepository(session)
    drivers_data = [
        {"name": "Lewis Hamilton", "nationality": "British"},
        {"name": "Max Verstappen", "nationality": "Dutch"},
        {"name": "Charles Leclerc", "nationality": "Monegasque"},
        {"name": "Carlos Sainz", "nationality": "Spanish"},
        {"name": "Lando Norris", "nationality": "British"},
    ]

    for dd in drivers_data:
        existing = driver_repo.get_by_name(dd["name"])
        if existing is None:
            driver = DriverModel(
                name=dd["name"],
                nationality=dd["nationality"],
            )
            session.add(driver)
            session.flush()

    # Create teams if they don't exist
    team_repo = TeamRepository(session)
    teams_data = [
        {"name": "Mercedes", "base_country": "United Kingdom"},
        {"name": "Red Bull Racing", "base_country": "Austria"},
        {"name": "Ferrari", "base_country": "Italy"},
        {"name": "McLaren", "base_country": "United Kingdom"},
        {"name": "Aston Martin", "base_country": "United Kingdom"},
    ]

    for td in teams_data:
        existing = team_repo.get_by_name(td["name"])
        if existing is None:
            team = TeamModel(
                name=td["name"],
                base_country=td["base_country"],
            )
            session.add(team)
            session.flush()

    # Create laps if they don't exist
    lap_repo = LapRepository(session)
    laps_data = [
        # Hamilton laps
        {
            "session_id": None,  # will set after sessions are created
            "driver_id": None,  # will set after drivers are created
            "team_id": None,  # will set after teams are created
            "lap_number": 1,
            "lap_time_seconds": 93.674,
            "sector_1_time_seconds": 32.145,
            "sector_2_time_seconds": 34.521,
            "sector_3_time_seconds": 26.987,
        },
        # Verstappen laps
        {
            "session_id": None,
            "driver_id": None,
            "team_id": None,
            "lap_number": 1,
            "lap_time_seconds": 93.602,
            "sector_1_time_seconds": 31.987,
            "sector_2_time_seconds": 34.412,
            "sector_3_time_seconds": 27.034,
        },
        # Leclerc laps
        {
            "session_id": None,
            "driver_id": None,
            "team_id": None,
            "lap_number": 1,
            "lap_time_seconds": 94.213,
            "sector_1_time_seconds": 32.456,
            "sector_2_time_seconds": 34.876,
            "sector_3_time_seconds": 27.123,
        },
    ]

    # Get the session and driver IDs we just created
    fp1_session = session_repo.get_by_race_and_type(race.race_id, "FP1")
    race_session = session_repo.get_by_race_and_type(race.race_id, "RACE")

    for ld in laps_data:
        # Find the right session_id
        target_session = None
        if ld.get("session_type") == "FP1":
            target_session = fp1_session
        elif ld.get("session_type") == "RACE":
            target_session = race_session

        if target_session is None:
            # Skip if we can't determine the session
            continue

        # Find the driver and team IDs
        driver_name = ld.get("driver_name", "Lewis Hamilton")
        driver = driver_repo.get_by_name(driver_name)
        if driver is None:
            continue

        team_name = ld.get("team_name", "Mercedes")
        team = team_repo.get_by_name(team_name)
        if team is None:
            continue

        # Check if lap already exists
        existing = lap_repo.get_by_session_driver_lap(
            target_session.session_id,
            driver.driver_id,
            ld["lap_number"],
        )
        if existing is not None:
            continue

        lap = LapModel(
            session_id=target_session.session_id,
            driver_id=driver.driver_id,
            team_id=team.team_id,
            lap_number=ld["lap_number"],
            lap_time_seconds=ld["lap_time_seconds"],
            sector_1_time_seconds=ld["sector_1_time_seconds"],
            sector_2_time_seconds=ld["sector_2_time_seconds"],
            sector_3_time_seconds=ld["sector_3_time_seconds"],
        )
        session.add(lap)


def main():
    """Main entry point for seeding historic data."""
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+pg8000://racepulse:racepulse@localhost:5432/racepulse?sslmode=require",
    )

    engine = create_engine(database_url, pool_pre_ping=True)

    # Create tables if they don't exist
    print("Creating tables if needed...")
    create_tables(engine)

    # Create session
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()

    try:
        print("Seeding limited historic data...")
        seed_data(session)
        session.commit()
        print("Done! Limited historic data seeded successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()