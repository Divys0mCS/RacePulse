# backend/tests/unit/test_csv_loader.py

import pytest

from analytics.loaders.csv_loader import CSVLoader

HEADER = (
    "season,round_number,race_name,track_name,track_country,track_length_km,"
    "track_corners,race_date,session_type,team_name,team_base_country,"
    "driver_number,driver_name,driver_nationality,lap_number,lap_time_seconds,"
    "sector_1_time_seconds,sector_2_time_seconds,sector_3_time_seconds\n"
)

ROW_TEMPLATE = (
    "2024,10,British Grand Prix,Silverstone,United Kingdom,5.891,18,"
    "2024-07-07,race,{team},{team_country},{number},{name},{nat},"
    "{lap_num},{lap_time},{sector_1},{sector_2},{sector_3}\n"
)


def write_csv(tmp_path, rows: list[str], header: str = HEADER):
    path = tmp_path / "laps.csv"
    path.write_text(header + "".join(rows))
    return path


def verstappen_row(lap_num, lap_time):
    return ROW_TEMPLATE.format(
        team="Red Bull Racing",
        team_country="Austria",
        number=1,
        name="Max Verstappen",
        nat="Dutch",
        lap_num=lap_num,
        lap_time=lap_time,
        sector_1=28.0,
        sector_2=30.0,
        sector_3=30.0,
    )


def hamilton_row(lap_num, lap_time):
    return ROW_TEMPLATE.format(
        team="Mercedes",
        team_country="Germany",
        number=44,
        name="Lewis Hamilton",
        nat="British",
        lap_num=lap_num,
        lap_time=lap_time,
        sector_1=30.0,
        sector_2=31.0,
        sector_3=30.2,
    )


def test_missing_file_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        CSVLoader().load("does/not/exist.csv")


def test_missing_column_raises_value_error(tmp_path):
    bad_header = "season,round_number,race_name\n"
    path = write_csv(tmp_path, ["2024,10,British Grand Prix\n"], header=bad_header)
    with pytest.raises(ValueError, match="missing required column"):
        CSVLoader().load(path)


def test_loads_one_lap_per_row(tmp_path):
    path = write_csv(tmp_path, [verstappen_row(1, 90.0), verstappen_row(2, 87.5)])
    laps = CSVLoader().load(path)
    assert len(laps) == 2
    assert [lap.lap_number for lap in laps] == [1, 2]
    assert laps[1].lap_time_seconds == 87.5

def test_loads_sector_times(tmp_path):
    path = write_csv(tmp_path, [verstappen_row(1, 88.0)])

    laps = CSVLoader().load(path)

    assert laps[0].sector_times == (28.0, 30.0, 30.0)


def test_same_driver_across_rows_is_one_shared_object(tmp_path):
    path = write_csv(tmp_path, [verstappen_row(1, 90.0), verstappen_row(2, 87.5)])
    laps = CSVLoader().load(path)
    assert laps[0].driver is laps[1].driver
    assert laps[0].driver.name == "Max Verstappen"


def test_same_race_session_across_rows_is_one_shared_object(tmp_path):
    path = write_csv(tmp_path, [verstappen_row(1, 90.0), hamilton_row(1, 91.2)])
    laps = CSVLoader().load(path)
    assert laps[0].session is laps[1].session
    assert laps[0].session.race.name == "British Grand Prix"


def test_different_drivers_get_different_objects(tmp_path):
    path = write_csv(tmp_path, [verstappen_row(1, 90.0), hamilton_row(1, 91.2)])
    laps = CSVLoader().load(path)
    assert laps[0].driver is not laps[1].driver
    assert laps[0].driver.team is not laps[1].driver.team


def test_malformed_lap_time_raises_value_error(tmp_path):
    bad_row = verstappen_row(1, "not-a-number")
    path = write_csv(tmp_path, [bad_row])
    with pytest.raises(ValueError, match="Row 2"):
        CSVLoader().load(path)

def test_add_lap_populates_session_laps(tmp_path):
    path = write_csv(tmp_path, [verstappen_row(1, 90.0), verstappen_row(2, 87.5)])
    laps = CSVLoader().load(path)
    session = laps[0].session
    assert len(session.laps) == 2
    assert laps[0] in session.laps
    assert laps[1] in session.laps


def test_invalid_session_type_raises_value_error(tmp_path):
    bad_row = ROW_TEMPLATE.format(
        team="Red Bull Racing",
        team_country="Austria",
        number=1,
        name="Max Verstappen",
        nat="Dutch",
        lap_num=1,
        lap_time=90.0,
        sector_1=28.0,
        sector_2=30.0,
        sector_3=32.0,
    ).replace(",race,", ",not_a_session,")

    path = write_csv(tmp_path, [bad_row])

    with pytest.raises(ValueError, match="Unrecognized session_type"):
        CSVLoader().load(path)