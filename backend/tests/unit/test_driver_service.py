from unittest.mock import MagicMock

import pytest

from app.database.models.driver import DriverModel
from app.database.services.driver_service import DriverService


def make_driver() -> DriverModel:
    return DriverModel(
        driver_id=1,
        name="Max Verstappen",
        nationality="Dutch",
    )


def test_create_driver_creates_commits_refreshes_and_returns_driver():
    db = MagicMock()
    service = DriverService(db)
    service.repository.create = MagicMock()

    result = service.create_driver(
        name="Max Verstappen",
        nationality="Dutch",
    )

    assert isinstance(result, DriverModel)
    assert result.name == "Max Verstappen"
    assert result.nationality == "Dutch"

    service.repository.create.assert_called_once_with(result)
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(result)


def test_create_driver_rolls_back_when_repository_fails():
    db = MagicMock()
    service = DriverService(db)

    service.repository.create = MagicMock(
        side_effect=RuntimeError("database error")
    )

    with pytest.raises(RuntimeError, match="database error"):
        service.create_driver(
            name="Max Verstappen",
            nationality="Dutch",
        )

    db.rollback.assert_called_once_with()
    db.commit.assert_not_called()


def test_get_driver_delegates_to_repository():
    db = MagicMock()
    service = DriverService(db)

    driver = make_driver()
    service.repository.get_by_id = MagicMock(return_value=driver)

    result = service.get_driver(1)

    assert result is driver
    service.repository.get_by_id.assert_called_once_with(1)


def test_get_driver_returns_none_when_not_found():
    db = MagicMock()
    service = DriverService(db)

    service.repository.get_by_id = MagicMock(return_value=None)

    result = service.get_driver(999)

    assert result is None
    service.repository.get_by_id.assert_called_once_with(999)


def test_list_drivers_delegates_to_repository():
    db = MagicMock()
    service = DriverService(db)

    drivers = [make_driver()]
    service.repository.list_all = MagicMock(return_value=drivers)

    result = service.list_drivers()

    assert result == drivers
    service.repository.list_all.assert_called_once_with()


def test_delete_driver_commits_when_driver_exists():
    db = MagicMock()
    service = DriverService(db)

    driver = make_driver()
    service.repository.get_by_id = MagicMock(return_value=driver)
    service.repository.delete = MagicMock()

    result = service.delete_driver(1)

    assert result is True
    service.repository.get_by_id.assert_called_once_with(1)
    service.repository.delete.assert_called_once_with(driver)
    db.commit.assert_called_once_with()


def test_delete_driver_returns_false_when_driver_does_not_exist():
    db = MagicMock()
    service = DriverService(db)

    service.repository.get_by_id = MagicMock(return_value=None)
    service.repository.delete = MagicMock()

    result = service.delete_driver(999)

    assert result is False
    service.repository.delete.assert_not_called()
    db.commit.assert_not_called()


def test_delete_driver_rolls_back_when_repository_fails():
    db = MagicMock()
    service = DriverService(db)

    driver = make_driver()
    service.repository.get_by_id = MagicMock(return_value=driver)
    service.repository.delete = MagicMock(
        side_effect=RuntimeError("delete failed")
    )

    with pytest.raises(RuntimeError, match="delete failed"):
        service.delete_driver(1)

    db.rollback.assert_called_once_with()