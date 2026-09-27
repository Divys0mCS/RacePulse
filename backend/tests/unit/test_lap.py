# backend/tests/unit/test_lap.py

import pytest
from datetime import date
from app.models.lap import Lap
from app.models.session import Session, SessionType
from app.models.race import Race
from app.models.track import Track
from app.models.driver import Driver
from app.models.team import Team


def make_session():
    track = Track(track_id=1, name="Silverstone", country="United Kingdom", length_km=5.891, number_of_corners=18)
    race = Race(race_id=1, name="British Grand Prix", season=2024, round_number=10, track=track, race_date=date(2024, 7, 7))
    return Session(session_id=1, race=race, session_type=SessionType.RACE)


def make_driver():
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    return Driver(driver_id=1, name="Max Verstappen", number=1, nationality="Dutch", team=team)


def make_lap(lap_id=1, session=None, driver=None, lap_number=1, lap_time_seconds=88.421, sector_times=None):
    return Lap(
        lap_id=lap_id,
        session=session or make_session(),
        driver=driver or make_driver(),
        lap_number=lap_number,
        lap_time_seconds=lap_time_seconds,
        sector_times=sector_times,
    )


def test_lap_creation():
    lap = make_lap()
    assert lap.lap_number == 1
    assert lap.lap_time_seconds == 88.421


def test_lap_repr():
    lap = make_lap()
    assert repr(lap) == "Lap(#1 Max Verstappen 88.421s)"


def test_lap_number_rejects_zero():
    with pytest.raises(ValueError):
        make_lap(lap_number=0)


def test_lap_time_rejects_zero_or_negative():
    with pytest.raises(ValueError):
        make_lap(lap_time_seconds=0)


def test_session_must_be_session_instance():
    with pytest.raises(TypeError):
        make_lap(session="Race Session")


def test_driver_must_be_driver_instance():
    with pytest.raises(TypeError):
        make_lap(driver="Max Verstappen")


def test_sector_times_must_have_three_positive_values():
    with pytest.raises(ValueError):
        make_lap(sector_times=(28.1, 30.2))


def test_sector_times_accepts_valid_tuple():
    lap = make_lap(sector_times=(28.1, 30.2, 30.1))
    assert lap.sector_times == (28.1, 30.2, 30.1)


def test_laps_compare_by_time():
    fast_lap = make_lap(lap_number=1, lap_time_seconds=87.0)
    slow_lap = make_lap(lap_number=2, lap_time_seconds=89.0)
    assert fast_lap < slow_lap
    assert not slow_lap < fast_lap


def test_laps_equal_by_time():
    lap_a = make_lap(lap_number=1, lap_time_seconds=88.0)
    lap_b = make_lap(lap_number=2, lap_time_seconds=88.0)
    assert lap_a == lap_b


def test_sorting_laps_by_time():
    laps = [make_lap(lap_number=1, lap_time_seconds=90.0),
            make_lap(lap_number=2, lap_time_seconds=87.5),
            make_lap(lap_number=3, lap_time_seconds=88.9)]
    ordered = sorted(laps)
    assert [lap.lap_number for lap in ordered] == [2, 3, 1]


def test_min_finds_fastest_lap():
    laps = [make_lap(lap_number=1, lap_time_seconds=90.0),
            make_lap(lap_number=2, lap_time_seconds=87.5),
            make_lap(lap_number=3, lap_time_seconds=88.9)]
    fastest = min(laps)
    assert fastest.lap_number == 2