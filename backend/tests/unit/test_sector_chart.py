import pytest
from datetime import date

from analytics.visualization.sector_chart import build_sector_chart
from app.models.lap import Lap
from app.models.session import Session, SessionType
from app.models.race import Race
from app.models.track import Track
from app.models.driver import Driver
from app.models.team import Team


def make_lap(lap_number, sector_times):
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
        lap_time_seconds=88.0,
        sector_times=sector_times,
    )


def test_build_sector_chart_raises_on_empty_laps():
    with pytest.raises(ValueError):
        build_sector_chart([])


def test_build_sector_chart_plots_all_three_sectors():
    laps = [
        make_lap(1, (28.0, 30.0, 30.0)),
        make_lap(2, (27.5, 29.8, 30.2)),
    ]

    fig = build_sector_chart(laps)

    assert len(fig.data) == 3

    assert list(fig.data[0].x) == [1, 2]
    assert list(fig.data[0].y) == [28.0, 27.5]

    assert list(fig.data[1].x) == [1, 2]
    assert list(fig.data[1].y) == [30.0, 29.8]

    assert list(fig.data[2].x) == [1, 2]
    assert list(fig.data[2].y) == [30.0, 30.2]


def test_build_sector_chart_sorts_laps_by_lap_number():
    laps = [
        make_lap(3, (29.0, 31.0, 30.5)),
        make_lap(1, (28.0, 30.0, 30.0)),
        make_lap(2, (27.5, 29.8, 30.2)),
    ]

    fig = build_sector_chart(laps)

    assert list(fig.data[0].x) == [1, 2, 3]
    assert list(fig.data[1].x) == [1, 2, 3]
    assert list(fig.data[2].x) == [1, 2, 3]


def test_build_sector_chart_has_sector_names():
    laps = [make_lap(1, (28.0, 30.0, 30.0))]

    fig = build_sector_chart(laps)

    names = [trace.name for trace in fig.data]

    assert names == ["Sector 1", "Sector 2", "Sector 3"]


def test_build_sector_chart_title_includes_driver():
    laps = [make_lap(1, (28.0, 30.0, 30.0))]

    fig = build_sector_chart(laps)

    assert "Max Verstappen" in fig.layout.title.text