from unittest.mock import MagicMock

import pytest

from app.database.models.driver import DriverModel
from app.database.models.lap import LapModel
from app.database.models.session import SessionModel
from app.database.models.team import TeamModel
from app.database.services.lap_service import (
    LapAlreadyExistsError,
    LapService,
)


def make_session() -> SessionModel:
    return SessionModel(
        session_id=1,
        race_id=10,
        session_type="RACE",
    )


def make_driver() -> DriverModel:
    return DriverModel(
        driver_id=2,
        name="Test Driver",
        nationality="Test Nationality",
    )


def make_team() -> TeamModel:
    return TeamModel(
        team_id=3,
        name="Test Team",
        base_country="Test Country",
    )


def make_lap() -> LapModel:
    return LapModel(
        lap_id=4,
        session_id=1,
        driver_id=2,
        team_id=3,
        lap_number=5,
        lap_time_seconds=92.345,
        sector_1_time_seconds=30.120,
        sector_2_time_seconds=31.210,
        sector_3_time_seconds=31.015,
    )


def test_create_lap_validates_dependencies_and_persists():
    db = MagicMock()
    service = LapService(db)

    service.session_repository.get_by_id = MagicMock(
        return_value=make_session()
    )
    service.driver_repository.get_by_id = MagicMock(
        return_value=make_driver()
    )
    service.team_repository.get_by_id = MagicMock(
        return_value=make_team()
    )
    service.repository.get_by_session_driver_lap = MagicMock(
        return_value=None
    )
    service.repository.create = MagicMock()

    result = service.create_lap(
        session_id=1,
        driver_id=2,
        team_id=3,
        lap_number=5,
        lap_time_seconds=92.345,
        sector_1_time_seconds=30.120,
        sector_2_time_seconds=31.210,
        sector_3_time_seconds=31.015,
    )

    assert isinstance(result, LapModel)
    assert result.session_id == 1
    assert result.driver_id == 2
    assert result.team_id == 3
    assert result.lap_number == 5
    assert result.lap_time_seconds == 92.345

    service.repository.create.assert_called_once_with(result)
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(result)


def test_create_lap_raises_when_session_does_not_exist():
    db = MagicMock()
    service = LapService(db)

    service.session_repository.get_by_id = MagicMock(
        return_value=None
    )
    service.repository.create = MagicMock()

    with pytest.raises(ValueError, match="Session 999 does not exist"):
        service.create_lap(
            session_id=999,
            driver_id=2,
            team_id=3,
            lap_number=1,
            lap_time_seconds=90.0,
            sector_1_time_seconds=30.0,
            sector_2_time_seconds=30.0,
            sector_3_time_seconds=30.0,
        )

    service.repository.create.assert_not_called()
    db.commit.assert_not_called()


def test_create_lap_raises_when_driver_does_not_exist():
    db = MagicMock()
    service = LapService(db)

    service.session_repository.get_by_id = MagicMock(
        return_value=make_session()
    )
    service.driver_repository.get_by_id = MagicMock(
        return_value=None
    )
    service.repository.create = MagicMock()

    with pytest.raises(ValueError, match="Driver 999 does not exist"):
        service.create_lap(
            session_id=1,
            driver_id=999,
            team_id=3,
            lap_number=1,
            lap_time_seconds=90.0,
            sector_1_time_seconds=30.0,
            sector_2_time_seconds=30.0,
            sector_3_time_seconds=30.0,
        )

    service.repository.create.assert_not_called()
    db.commit.assert_not_called()


def test_create_lap_raises_when_team_does_not_exist():
    db = MagicMock()
    service = LapService(db)

    service.session_repository.get_by_id = MagicMock(
        return_value=make_session()
    )
    service.driver_repository.get_by_id = MagicMock(
        return_value=make_driver()
    )
    service.team_repository.get_by_id = MagicMock(
        return_value=None
    )
    service.repository.create = MagicMock()

    with pytest.raises(ValueError, match="Team 999 does not exist"):
        service.create_lap(
            session_id=1,
            driver_id=2,
            team_id=999,
            lap_number=1,
            lap_time_seconds=90.0,
            sector_1_time_seconds=30.0,
            sector_2_time_seconds=30.0,
            sector_3_time_seconds=30.0,
        )

    service.repository.create.assert_not_called()
    db.commit.assert_not_called()


def test_create_lap_raises_when_duplicate_exists():
    db = MagicMock()
    service = LapService(db)

    service.session_repository.get_by_id = MagicMock(
        return_value=make_session()
    )
    service.driver_repository.get_by_id = MagicMock(
        return_value=make_driver()
    )
    service.team_repository.get_by_id = MagicMock(
        return_value=make_team()
    )
    service.repository.get_by_session_driver_lap = MagicMock(
        return_value=make_lap()
    )
    service.repository.create = MagicMock()

    with pytest.raises(
        LapAlreadyExistsError,
        match="Lap already exists for this session, driver, and lap number",
    ):
        service.create_lap(
            session_id=1,
            driver_id=2,
            team_id=3,
            lap_number=5,
            lap_time_seconds=92.345,
            sector_1_time_seconds=30.120,
            sector_2_time_seconds=31.210,
            sector_3_time_seconds=31.015,
        )

    service.repository.create.assert_not_called()
    db.commit.assert_not_called()


def test_create_lap_rolls_back_when_repository_fails():
    db = MagicMock()
    service = LapService(db)

    service.session_repository.get_by_id = MagicMock(
        return_value=make_session()
    )
    service.driver_repository.get_by_id = MagicMock(
        return_value=make_driver()
    )
    service.team_repository.get_by_id = MagicMock(
        return_value=make_team()
    )
    service.repository.get_by_session_driver_lap = MagicMock(
        return_value=None
    )
    service.repository.create = MagicMock(
        side_effect=RuntimeError("database error")
    )

    with pytest.raises(RuntimeError, match="database error"):
        service.create_lap(
            session_id=1,
            driver_id=2,
            team_id=3,
            lap_number=5,
            lap_time_seconds=92.345,
            sector_1_time_seconds=30.120,
            sector_2_time_seconds=31.210,
            sector_3_time_seconds=31.015,
        )

    db.rollback.assert_called_once_with()
    db.commit.assert_not_called()


def test_get_lap_delegates_to_repository():
    db = MagicMock()
    service = LapService(db)

    lap = make_lap()
    service.repository.get_by_id = MagicMock(return_value=lap)

    result = service.get_lap(4)

    assert result is lap
    service.repository.get_by_id.assert_called_once_with(4)


def test_get_lap_by_session_driver_lap_delegates_to_repository():
    db = MagicMock()
    service = LapService(db)

    lap = make_lap()
    service.repository.get_by_session_driver_lap = MagicMock(
        return_value=lap
    )

    result = service.get_lap_by_session_driver_lap(
        session_id=1,
        driver_id=2,
        lap_number=5,
    )

    assert result is lap
    service.repository.get_by_session_driver_lap.assert_called_once_with(
        1,
        2,
        5,
    )


def test_list_laps_by_session_delegates_to_repository():
    db = MagicMock()
    service = LapService(db)

    laps = [make_lap()]
    service.repository.list_by_session = MagicMock(
        return_value=laps
    )

    result = service.list_laps_by_session(
        session_id=1,
        skip=20,
        limit=10,
    )

    assert result == laps

    service.repository.list_by_session.assert_called_once_with(
        1,
        skip=20,
        limit=10,
    )


def test_list_laps_delegates_to_repository():
    db = MagicMock()
    service = LapService(db)

    laps = [make_lap()]
    service.repository.list_all = MagicMock(
        return_value=laps
    )

    result = service.list_laps(
        skip=20,
        limit=10,
    )

    assert result == laps

    service.repository.list_all.assert_called_once_with(
        skip=20,
        limit=10,
    )


def test_delete_lap_commits_when_lap_exists():
    db = MagicMock()
    service = LapService(db)

    lap = make_lap()

    service.repository.get_by_id = MagicMock(return_value=lap)
    service.repository.delete = MagicMock()

    result = service.delete_lap(4)

    assert result is True
    service.repository.get_by_id.assert_called_once_with(4)
    service.repository.delete.assert_called_once_with(lap)
    db.commit.assert_called_once_with()


def test_delete_lap_returns_false_when_lap_does_not_exist():
    db = MagicMock()
    service = LapService(db)

    service.repository.get_by_id = MagicMock(return_value=None)
    service.repository.delete = MagicMock()

    result = service.delete_lap(999)

    assert result is False
    service.repository.delete.assert_not_called()
    db.commit.assert_not_called()


def test_delete_lap_rolls_back_when_repository_fails():
    db = MagicMock()
    service = LapService(db)

    lap = make_lap()

    service.repository.get_by_id = MagicMock(return_value=lap)
    service.repository.delete = MagicMock(
        side_effect=RuntimeError("delete failed")
    )

    with pytest.raises(RuntimeError, match="delete failed"):
        service.delete_lap(4)

    db.rollback.assert_called_once_with()