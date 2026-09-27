import pytest
from datetime import date
from app.models.race import Race
from app.models.track import Track


def make_track():
    return Track(track_id=1, name="Silverstone", country="United Kingdom", length_km=5.891, number_of_corners=18)


def make_race(race_id=1, name="British Grand Prix", season=2024, round_number=10, track=None, race_date=date(2024, 7, 7)):
    return Race(race_id=race_id, name=name, season=season, round_number=round_number, track=track or make_track(), race_date=race_date)


def test_race_creation():
    r = make_race()
    assert r.name == "British Grand Prix"
    assert r.track.name == "Silverstone"


def test_race_repr():
    r = make_race()
    assert repr(r) == "Race(British Grand Prix, 2024 Round 10, Silverstone)"


def test_season_rejects_before_1950():
    with pytest.raises(ValueError):
        make_race(season=1949)


def test_round_number_rejects_zero():
    with pytest.raises(ValueError):
        make_race(round_number=0)


def test_race_date_is_stored():
    r = make_race(race_date=date(2024, 7, 7))
    assert r.race_date == date(2024, 7, 7)

def test_track_must_be_track_instance():
    with pytest.raises(TypeError):
        make_race(track="Silverstone")