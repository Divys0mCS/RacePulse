import pytest
from datetime import date
from dataclasses import FrozenInstanceError
from app.models.telemetry import Telemetry, TelemetrySample
from app.models.lap import Lap
from app.models.session import Session, SessionType
from app.models.race import Race
from app.models.track import Track
from app.models.driver import Driver
from app.models.team import Team


def make_lap():
    track = Track(track_id=1, name="Silverstone", country="United Kingdom", length_km=5.891, number_of_corners=18)
    race = Race(race_id=1, name="British Grand Prix", season=2024, round_number=10, track=track, race_date=date(2024, 7, 7))
    session = Session(session_id=1, race=race, session_type=SessionType.RACE)
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    driver = Driver(driver_id=1, name="Max Verstappen", number=1, nationality="Dutch", team=team)
    return Lap(lap_id=1, session=session, driver=driver, lap_number=1, lap_time_seconds=88.421)


def make_sample(distance_m=0.0, speed_kph=250.0, throttle_pct=100.0, brake_pct=0.0, gear=7, rpm=11500):
    return TelemetrySample(distance_m=distance_m, speed_kph=speed_kph, throttle_pct=throttle_pct, brake_pct=brake_pct, gear=gear, rpm=rpm)


def test_telemetry_sample_creation():
    s = make_sample()
    assert s.speed_kph == 250.0
    assert s.gear == 7


def test_telemetry_sample_is_immutable():
    s = make_sample()
    with pytest.raises(FrozenInstanceError):
        s.speed_kph = 999


def test_telemetry_sample_equality_is_by_value():
    assert make_sample() == make_sample()  # dataclass gives value-based equality for free


def test_telemetry_sample_rejects_invalid_throttle():
    with pytest.raises(ValueError):
        make_sample(throttle_pct=150)


def test_telemetry_sample_rejects_negative_speed():
    with pytest.raises(ValueError):
        make_sample(speed_kph=-1)


def test_telemetry_creation():
    t = Telemetry(telemetry_id=1, lap=make_lap())
    assert t.samples == []


def test_telemetry_repr():
    t = Telemetry(telemetry_id=1, lap=make_lap())
    assert repr(t) == "Telemetry(lap=#1, 0 sample(s))"


def test_lap_must_be_lap_instance():
    with pytest.raises(TypeError):
        Telemetry(telemetry_id=1, lap="Lap 1")


def test_add_sample_appends():
    t = Telemetry(telemetry_id=1, lap=make_lap())
    t.add_sample(make_sample())
    assert len(t.samples) == 1


def test_add_sample_rejects_wrong_type():
    t = Telemetry(telemetry_id=1, lap=make_lap())
    with pytest.raises(TypeError):
        t.add_sample("not a sample")


def test_max_speed_with_no_samples_is_none():
    assert Telemetry(telemetry_id=1, lap=make_lap()).max_speed_kph() is None


def test_max_speed_kph():
    t = Telemetry(telemetry_id=1, lap=make_lap())
    for speed in (250, 310, 180):
        t.add_sample(make_sample(speed_kph=speed))
    assert t.max_speed_kph() == 310


def test_average_throttle_with_no_samples_is_none():
    assert Telemetry(telemetry_id=1, lap=make_lap()).average_throttle_pct() is None


def test_average_throttle_pct():
    t = Telemetry(telemetry_id=1, lap=make_lap())
    t.add_sample(make_sample(throttle_pct=100))
    t.add_sample(make_sample(throttle_pct=50))
    assert t.average_throttle_pct() == 75