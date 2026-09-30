from sqlalchemy import inspect

from app.database.base import Base
from app.database.models.driver import DriverModel


def test_driver_model_uses_drivers_table() -> None:
    assert DriverModel.__tablename__ == "drivers"


def test_driver_model_inherits_from_base() -> None:
    assert issubclass(DriverModel, Base)


def test_driver_model_has_expected_columns() -> None:
    columns = set(DriverModel.__table__.columns.keys())

    assert columns == {
        "driver_id",
        "name",
        "nationality",
    }


def test_driver_id_is_primary_key() -> None:
    primary_keys = {
        column.name
        for column in inspect(DriverModel).primary_key
    }

    assert primary_keys == {"driver_id"}


def test_driver_columns_are_non_nullable() -> None:
    for column in DriverModel.__table__.columns:
        assert column.nullable is False