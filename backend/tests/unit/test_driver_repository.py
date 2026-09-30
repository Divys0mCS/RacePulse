from unittest.mock import MagicMock

from app.database.models.driver import DriverModel
from app.database.repositories.driver_repository import DriverRepository


def make_driver() -> DriverModel:
    return DriverModel(
        driver_id=1,
        name="Max Verstappen",
        nationality="Dutch",
    )


def test_create_adds_and_flushes_driver():
    db = MagicMock()
    repository = DriverRepository(db)

    driver = make_driver()

    result = repository.create(driver)

    assert result is driver
    db.add.assert_called_once_with(driver)
    db.flush.assert_called_once_with()


def test_get_by_id_uses_session_get():
    db = MagicMock()

    driver = make_driver()
    db.get.return_value = driver

    repository = DriverRepository(db)

    result = repository.get_by_id(1)

    assert result is driver
    db.get.assert_called_once_with(DriverModel, 1)


def test_get_by_id_returns_none_when_not_found():
    db = MagicMock()
    db.get.return_value = None

    repository = DriverRepository(db)

    result = repository.get_by_id(999)

    assert result is None
    db.get.assert_called_once_with(DriverModel, 999)


def test_list_all_returns_drivers():
    db = MagicMock()

    driver = make_driver()

    scalars = MagicMock()
    scalars.all.return_value = [driver]
    db.scalars.return_value = scalars

    repository = DriverRepository(db)

    result = repository.list_all()

    assert result == [driver]
    db.scalars.assert_called_once()


def test_list_all_applies_pagination():
    db = MagicMock()

    driver = make_driver()

    scalars = MagicMock()
    scalars.all.return_value = [driver]
    db.scalars.return_value = scalars

    repository = DriverRepository(db)

    result = repository.list_all(
        skip=20,
        limit=10,
    )

    assert result == [driver]
    db.scalars.assert_called_once()


def test_delete_delegates_to_session():
    db = MagicMock()
    repository = DriverRepository(db)

    driver = make_driver()

    repository.delete(driver)

    db.delete.assert_called_once_with(driver)