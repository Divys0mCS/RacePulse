# backend/tests/unit/test_session.py

import pytest
from datetime import date
from app.models.session import Session, SessionType
from app.models.race import Race
from app.models.track import Track


def make_race():
    track = Track(track_id=1, name="Silverstone", country="United Kingdom", length_km=5.891, number_of_corners=18)
    return Race(race_id=1, name="British Grand Prix", season=2024, round_number=10, track=track, race_date=date(2024, 7, 7))


def test_session_creation():
    s = Session(session_id=1, race=make_race(), session_type=SessionType.RACE)
    assert s.session_type is SessionType.RACE
    assert s.laps == []


def test_session_repr():
    s = Session(session_id=1, race=make_race(), session_type=SessionType.QUALIFYING)
    assert repr(s) == "Session(Qualifying, British Grand Prix)"


def test_invalid_session_type_raises():
    with pytest.raises(TypeError):
        Session(session_id=1, race=make_race(), session_type="Race")  # plain string, not SessionType


def test_add_lap_appends():
    s = Session(session_id=1, race=make_race(), session_type=SessionType.RACE)
    fake_lap = object()  # stand-in until Lap exists
    s.add_lap(fake_lap)
    assert fake_lap in s.laps


def test_add_lap_does_not_duplicate():
    s = Session(session_id=1, race=make_race(), session_type=SessionType.RACE)
    fake_lap = object()
    s.add_lap(fake_lap)
    s.add_lap(fake_lap)
    assert s.laps.count(fake_lap) == 1

def test_race_must_be_race_instance():
    with pytest.raises(TypeError):
        Session(session_id=1, race="British Grand Prix", session_type=SessionType.RACE)