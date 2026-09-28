import pytest
from datetime import date

from analytics.visualization.lap_chart import build_lap_chart
from app.models.lap import Lap
from app.models.session import Session, SessionType
from app.models.race import Race
from app.models.track import Track
from app.models.driver import Driver
from app.models.team import Team


def make_lap(lap_number, lap_time_seconds):
    track = Track(
        track_id=1,
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )

    race = Race(
        race_id=1,
        name="British Grand Prix",
        season=2024,
        round_number=10,
        track=track,
        race_date=date(2024, 7, 7),
    )

    session = Session(
        session_id=1,
        race=race,
        session_type=SessionType.RACE,
    )

    team = Team(
        team_id=1,
        name="Red Bull Racing",
        base_country="Austria",
    )

    driver = Driver(
        driver_id=1,
        name="Max Verstappen",
        number=1,
        nationality="Dutch",
        team=team,
    )

    return Lap(
        lap_id=lap_number,
        session=session,
        driver=driver,
        lap_number=lap_number,
        lap_time_seconds=lap_time_seconds,
    )


def test_build_lap_chart_raises_on_empty_laps():
    with pytest.raises(ValueError):
        build_lap_chart([])


def test_build_lap_chart_plots_lap_number_vs_lap_time():
    laps = [
        make_lap(1, 90.0),
        make_lap(2, 87.5),
        make_lap(3, 88.9),
    ]

    fig = build_lap_chart(laps)

    assert list(fig.data[0].x) == [1, 2, 3]
    assert list(fig.data[0].y) == [90.0, 87.5, 88.9]


def test_build_lap_chart_sorts_laps_by_lap_number():
    laps = [
        make_lap(3, 88.9),
        make_lap(1, 90.0),
        make_lap(2, 87.5),
    ]

    fig = build_lap_chart(laps)

    assert list(fig.data[0].x) == [1, 2, 3]
    assert list(fig.data[0].y) == [90.0, 87.5, 88.9]


def test_build_lap_chart_title_includes_driver():
    laps = [make_lap(1, 90.0)]

    fig = build_lap_chart(laps)

    assert "Max Verstappen" in fig.layout.title.text