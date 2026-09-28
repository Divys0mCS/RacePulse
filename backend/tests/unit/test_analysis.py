import pytest
from datetime import date
from analytics.analysis.base_analyzer import BaseAnalyzer
from analytics.analysis.pace_analysis import PaceAnalyzer
from app.models.lap import Lap
from app.models.session import Session, SessionType
from app.models.race import Race
from app.models.track import Track
from app.models.driver import Driver
from app.models.team import Team
from analytics.analysis.sector_analysis import SectorAnalyzer
from analytics.analysis.lap_analysis import LapAnalyzer

def make_session():
    track = Track(track_id=1, name="Silverstone", country="United Kingdom", length_km=5.891, number_of_corners=18)
    race = Race(race_id=1, name="British Grand Prix", season=2024, round_number=10, track=track, race_date=date(2024, 7, 7))
    return Session(session_id=1, race=race, session_type=SessionType.RACE)


def make_driver():
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    return Driver(driver_id=1, name="Max Verstappen", number=1, nationality="Dutch", team=team)


def make_lap(lap_number, lap_time_seconds, sector_times=None):
    return Lap(
        lap_id=lap_number,
        session=make_session(),
        driver=make_driver(),
        lap_number=lap_number,
        lap_time_seconds=lap_time_seconds,
        sector_times=sector_times,
    )

def test_sector_analyzer_is_a_base_analyzer():

    assert isinstance(SectorAnalyzer(), BaseAnalyzer)


def test_sector_analyzer_with_no_laps():

    result = SectorAnalyzer().analyze([])

    assert result == {
        "fastest_sector_1_seconds": None,
        "fastest_sector_2_seconds": None,
        "fastest_sector_3_seconds": None,
        "laps_analyzed": 0,
    }


def test_sector_analyzer_finds_fastest_time_in_each_sector():

    laps = [
        make_lap(1, 90.0, sector_times=(29.5, 31.0, 29.5)),
        make_lap(2, 87.5, sector_times=(28.4, 30.1, 29.0)),
        make_lap(3, 88.9, sector_times=(28.8, 30.4, 29.7)),
    ]

    result = SectorAnalyzer().analyze(laps)

    assert result["fastest_sector_1_seconds"] == 28.4
    assert result["fastest_sector_2_seconds"] == 30.1
    assert result["fastest_sector_3_seconds"] == 29.0
    assert result["laps_analyzed"] == 3

def test_base_analyzer_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        BaseAnalyzer()


def test_pace_analyzer_is_a_base_analyzer():
    assert isinstance(PaceAnalyzer(), BaseAnalyzer)


def test_pace_analyzer_with_no_laps():
    result = PaceAnalyzer().analyze([])
    assert result == {"fastest_lap": None, "average_lap_time_seconds": None, "laps_analyzed": 0}


def test_pace_analyzer_finds_fastest_lap():
    laps = [make_lap(1, 90.0), make_lap(2, 87.5), make_lap(3, 88.9)]
    result = PaceAnalyzer().analyze(laps)
    assert result["fastest_lap"].lap_number == 2


def test_pace_analyzer_average_lap_time():
    laps = [make_lap(1, 90.0), make_lap(2, 90.0), make_lap(3, 90.0)]
    result = PaceAnalyzer().analyze(laps)
    assert result["average_lap_time_seconds"] == 90.0


def test_pace_analyzer_laps_analyzed_count():
    laps = [make_lap(1, 90.0), make_lap(2, 87.5)]
    result = PaceAnalyzer().analyze(laps)
    assert result["laps_analyzed"] == 2


def test_polymorphism_any_base_analyzer_can_be_called_uniformly():
    analyzers: list[BaseAnalyzer] = [PaceAnalyzer()]  # more subclasses join this list later
    laps = [make_lap(1, 90.0), make_lap(2, 87.5)]
    results = [analyzer.analyze(laps) for analyzer in analyzers]
    assert results[0]["laps_analyzed"] == 2

from analytics.analysis.consistency_analysis import ConsistencyAnalyzer


def test_consistency_analyzer_is_a_base_analyzer():
    assert isinstance(ConsistencyAnalyzer(), BaseAnalyzer)


def test_consistency_analyzer_with_no_laps():
    result = ConsistencyAnalyzer().analyze([])
    assert result == {"consistency_stdev_seconds": None, "laps_analyzed": 0}


def test_consistency_analyzer_with_one_lap():
    result = ConsistencyAnalyzer().analyze([make_lap(1, 90.0)])
    assert result == {"consistency_stdev_seconds": None, "laps_analyzed": 1}


def test_consistency_analyzer_identical_laps_have_zero_stdev():
    laps = [make_lap(1, 90.0), make_lap(2, 90.0), make_lap(3, 90.0)]
    result = ConsistencyAnalyzer().analyze(laps)
    assert result["consistency_stdev_seconds"] == 0.0


def test_consistency_analyzer_detects_variation():
    consistent = [make_lap(1, 90.0), make_lap(2, 90.1), make_lap(3, 89.9)]
    erratic = [make_lap(1, 87.0), make_lap(2, 93.0), make_lap(3, 90.0)]
    consistent_result = ConsistencyAnalyzer().analyze(consistent)
    erratic_result = ConsistencyAnalyzer().analyze(erratic)
    assert consistent_result["consistency_stdev_seconds"] < erratic_result["consistency_stdev_seconds"]

def test_lap_analyzer_is_a_base_analyzer():
    assert isinstance(LapAnalyzer(), BaseAnalyzer)


def test_lap_analyzer_with_no_laps():
    result = LapAnalyzer().analyze([])

    assert result == {
        "laps_analyzed": 0,
        "lap_times_seconds": [],
        "lap_time_deltas_seconds": [],
    }


def test_lap_analyzer_returns_lap_times_in_lap_order():
    laps = [
        make_lap(3, 88.9),
        make_lap(1, 90.0),
        make_lap(2, 87.5),
    ]

    result = LapAnalyzer().analyze(laps)

    assert result["laps_analyzed"] == 3
    assert result["lap_times_seconds"] == [90.0, 87.5, 88.9]


def test_lap_analyzer_calculates_consecutive_lap_deltas():
    laps = [
        make_lap(1, 90.0),
        make_lap(2, 87.5),
        make_lap(3, 88.9),
    ]

    result = LapAnalyzer().analyze(laps)

    assert result["lap_time_deltas_seconds"] == [-2.5, 1.4]
def test_lap_analyzer_with_one_lap():
    result = LapAnalyzer().analyze([make_lap(1, 90.0)])

    assert result == {
        "laps_analyzed": 1,
        "lap_times_seconds": [90.0],
        "lap_time_deltas_seconds": [],
    }