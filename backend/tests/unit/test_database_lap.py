from sqlalchemy import inspect

from app.database.base import Base
from app.database.models.lap import LapModel


def test_lap_model_uses_laps_table() -> None:
    assert LapModel.__tablename__ == "laps"


def test_lap_model_inherits_from_base() -> None:
    assert issubclass(LapModel, Base)


def test_lap_model_has_expected_columns() -> None:
    columns = set(LapModel.__table__.columns.keys())

    assert columns == {
        "lap_id",
        "session_id",
        "driver_id",
        "team_id",
        "lap_number",
        "lap_time_seconds",
        "sector_1_time_seconds",
        "sector_2_time_seconds",
        "sector_3_time_seconds",
    }


def test_lap_id_is_primary_key() -> None:
    primary_keys = {
        column.name
        for column in inspect(LapModel).primary_key
    }

    assert primary_keys == {"lap_id"}


def test_lap_columns_are_non_nullable() -> None:
    for column in LapModel.__table__.columns:
        assert column.nullable is False


def test_lap_has_expected_foreign_keys() -> None:
    foreign_keys = {
        foreign_key.target_fullname
        for foreign_key in LapModel.__table__.foreign_keys
    }

    assert foreign_keys == {
        "sessions.session_id",
        "drivers.driver_id",
        "teams.team_id",
    }


def test_lap_has_expected_constraints() -> None:
    constraint_names = {
        constraint.name
        for constraint in LapModel.__table__.constraints
        if constraint.name is not None
    }

    assert "ck_laps_lap_number_positive" in constraint_names
    assert "ck_laps_lap_time_positive" in constraint_names
    assert "ck_laps_sector_1_positive" in constraint_names
    assert "ck_laps_sector_2_positive" in constraint_names
    assert "ck_laps_sector_3_positive" in constraint_names
    assert "uq_laps_session_driver_lap" in constraint_names