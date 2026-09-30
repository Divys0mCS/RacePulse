from unittest.mock import MagicMock

from app.database.models.lap import LapModel
from app.database.repositories.lap_repository import LapRepository


def make_lap() -> LapModel:
    return LapModel(
        lap_id=1,
        session_id=10,
        driver_id=20,
        team_id=30,
        lap_number=5,
        lap_time_seconds=92.345,
        sector_1_time_seconds=30.120,
        sector_2_time_seconds=31.210,
        sector_3_time_seconds=31.015,
    )


def test_create_adds_and_flushes_lap():
    db = MagicMock()
    repository = LapRepository(db)

    lap = make_lap()

    result = repository.create(lap)

    assert result is lap
    db.add.assert_called_once_with(lap)
    db.flush.assert_called_once_with()


def test_get_by_id_uses_session_get():
    db = MagicMock()
    lap = make_lap()
    db.get.return_value = lap

    repository = LapRepository(db)

    result = repository.get_by_id(1)

    assert result is lap
    db.get.assert_called_once_with(LapModel, 1)


def test_get_by_id_returns_none_when_not_found():
    db = MagicMock()
    db.get.return_value = None

    repository = LapRepository(db)

    result = repository.get_by_id(999)

    assert result is None
    db.get.assert_called_once_with(LapModel, 999)


def test_get_by_session_driver_lap_returns_lap():
    db = MagicMock()
    lap = make_lap()
    db.scalar.return_value = lap

    repository = LapRepository(db)

    result = repository.get_by_session_driver_lap(
        session_id=10,
        driver_id=20,
        lap_number=5,
    )

    assert result is lap
    db.scalar.assert_called_once()


def test_get_by_session_driver_lap_returns_none_when_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    repository = LapRepository(db)

    result = repository.get_by_session_driver_lap(
        session_id=10,
        driver_id=20,
        lap_number=999,
    )

    assert result is None
    db.scalar.assert_called_once()


def test_list_by_session_returns_laps():
    db = MagicMock()

    lap_1 = make_lap()
    lap_2 = LapModel(
        lap_id=2,
        session_id=10,
        driver_id=20,
        team_id=30,
        lap_number=6,
        lap_time_seconds=91.900,
        sector_1_time_seconds=29.900,
        sector_2_time_seconds=31.000,
        sector_3_time_seconds=31.000,
    )

    scalars = MagicMock()
    scalars.all.return_value = [lap_1, lap_2]
    db.scalars.return_value = scalars

    repository = LapRepository(db)

    result = repository.list_by_session(10)

    assert result == [lap_1, lap_2]
    db.scalars.assert_called_once()


def test_list_all_returns_laps():
    db = MagicMock()

    lap = make_lap()

    scalars = MagicMock()
    scalars.all.return_value = [lap]
    db.scalars.return_value = scalars

    repository = LapRepository(db)

    result = repository.list_all()

    assert result == [lap]
    db.scalars.assert_called_once()


def test_delete_delegates_to_session():
    db = MagicMock()
    repository = LapRepository(db)

    lap = make_lap()

    repository.delete(lap)

    db.delete.assert_called_once_with(lap)