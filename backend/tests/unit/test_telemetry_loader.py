import pytest
from datetime import date
from analytics.loaders.telemetry_loader import TelemetryLoader
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


def make_driver(number=1, name="Max Verstappen"):
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    return Driver(driver_id=number, name=name, number=number, nationality="Dutch", team=team)


def make_lap(lap_id, driver_number, lap_number):
    return Lap(lap_id=lap_id, session=make_session(), driver=make_driver(number=driver_number),
               lap_number=lap_number, lap_time_seconds=88.0)


HEADER = "driver_number,lap_number,distance_m,speed_kph,throttle_pct,brake_pct,gear,rpm\n"


def row(driver_number, lap_number, distance_m, speed_kph, throttle_pct=100, brake_pct=0, gear=7, rpm=11000):
    return f"{driver_number},{lap_number},{distance_m},{speed_kph},{throttle_pct},{brake_pct},{gear},{rpm}\n"


def write_csv(tmp_path, rows, header=HEADER):
    path = tmp_path / "telemetry.csv"
    path.write_text(header + "".join(rows))
    return path


def test_missing_file_raises_file_not_found():
    laps = [make_lap(1, driver_number=1, lap_number=1)]
    with pytest.raises(FileNotFoundError):
        TelemetryLoader(laps).load("does/not/exist.csv")


def test_missing_column_raises_value_error(tmp_path):
    laps = [make_lap(1, driver_number=1, lap_number=1)]
    path = write_csv(tmp_path, ["1,1\n"], header="driver_number,lap_number\n")
    with pytest.raises(ValueError, match="missing required column"):
        TelemetryLoader(laps).load(path)


def test_samples_attach_to_matching_lap(tmp_path):
    lap = make_lap(1, driver_number=1, lap_number=1)
    path = write_csv(tmp_path, [row(1, 1, 0, 250), row(1, 1, 100, 280)])
    telemetry_list = TelemetryLoader([lap]).load(path)

    assert len(telemetry_list) == 1
    telemetry = telemetry_list[0]
    assert telemetry.lap is lap
    assert len(telemetry.samples) == 2
    assert telemetry.max_speed_kph() == 280


def test_samples_for_different_laps_get_separate_telemetry(tmp_path):
    lap1 = make_lap(1, driver_number=1, lap_number=1)
    lap2 = make_lap(2, driver_number=1, lap_number=2)
    path = write_csv(tmp_path, [row(1, 1, 0, 250), row(1, 2, 0, 260)])
    telemetry_list = TelemetryLoader([lap1, lap2]).load(path)

    assert len(telemetry_list) == 2
    by_lap = {t.lap.lap_id: t for t in telemetry_list}
    assert by_lap[1].samples[0].speed_kph == 250
    assert by_lap[2].samples[0].speed_kph == 260


def test_unmatched_lap_raises_value_error(tmp_path):
    lap = make_lap(1, driver_number=1, lap_number=1)
    path = write_csv(tmp_path, [row(1, 99, 0, 250)])  # lap_number 99 doesn't exist
    with pytest.raises(ValueError, match="No matching lap"):
        TelemetryLoader([lap]).load(path)


def test_malformed_speed_raises_value_error(tmp_path):
    lap = make_lap(1, driver_number=1, lap_number=1)
    path = write_csv(tmp_path, [row(1, 1, 0, "fast")])
    with pytest.raises(ValueError, match="Row 2"):
        TelemetryLoader([lap]).load(path)