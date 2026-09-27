import pytest
from datetime import date
from analytics.visualization.speed_trace import build_speed_trace
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
    return Lap(lap_id=1, session=session, driver=driver, lap_number=2, lap_time_seconds=87.5)


def make_sample(distance_m, speed_kph):
    return TelemetrySample(distance_m=distance_m, speed_kph=speed_kph, throttle_pct=100, brake_pct=0, gear=7, rpm=11500)


def test_build_speed_trace_raises_on_empty_samples():
    telemetry = Telemetry(telemetry_id=1, lap=make_lap())
    with pytest.raises(ValueError):
        build_speed_trace(telemetry)


def test_build_speed_trace_plots_distance_vs_speed():
    telemetry = Telemetry(telemetry_id=1, lap=make_lap())
    telemetry.add_sample(make_sample(0, 120))
    telemetry.add_sample(make_sample(500, 265))
    telemetry.add_sample(make_sample(1200, 310))

    fig = build_speed_trace(telemetry)

    assert list(fig.data[0].x) == [0, 500, 1200]
    assert list(fig.data[0].y) == [120, 265, 310]


def test_build_speed_trace_sorts_out_of_order_samples():
    telemetry = Telemetry(telemetry_id=1, lap=make_lap())
    telemetry.add_sample(make_sample(1200, 310))  # added out of distance order on purpose
    telemetry.add_sample(make_sample(0, 120))

    fig = build_speed_trace(telemetry)

    assert list(fig.data[0].x) == [0, 1200]


def test_build_speed_trace_title_includes_driver_and_lap():
    telemetry = Telemetry(telemetry_id=1, lap=make_lap())
    telemetry.add_sample(make_sample(0, 120))

    fig = build_speed_trace(telemetry)

    assert "Max Verstappen" in fig.layout.title.text
    assert "Lap 2" in fig.layout.title.text