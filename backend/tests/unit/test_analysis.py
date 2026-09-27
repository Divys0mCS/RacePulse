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


def make_session():
    track = Track(track_id=1, name="Silverstone", country="United Kingdom", length_km=5.891, number_of_corners=18)
    race = Race(race_id=1, name="British Grand Prix", season=2024, round_number=10, track=track, race_date=date(2024, 7, 7))
    return Session(session_id=1, race=race, session_type=SessionType.RACE)


def make_driver():
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    return Driver(driver_id=1, name="Max Verstappen", number=1, nationality="Dutch", team=team)


def make_lap(lap_number, lap_time_seconds):
    return Lap(lap_id=lap_number, session=make_session(), driver=make_driver(), lap_number=lap_number, lap_time_seconds=lap_time_seconds)


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