from datetime import date
from unittest.mock import MagicMock

from app.database.models.race import RaceModel
from app.database.repositories.race_repository import RaceRepository


def test_create_adds_and_flushes_race():
    db = MagicMock()
    repository = RaceRepository(db)

    race = RaceModel(
        name="British Grand Prix",
        season=2026,
        round_number=12,
        track_id=1,
        race_date=date(2026, 7, 5),
    )

    result = repository.create(race)

    assert result is race
    db.add.assert_called_once_with(race)
    db.flush.assert_called_once_with()


def test_get_by_id_uses_session_get():
    db = MagicMock()

    race = RaceModel(
        race_id=1,
        name="British Grand Prix",
        season=2026,
        round_number=12,
        track_id=1,
        race_date=date(2026, 7, 5),
    )

    db.get.return_value = race

    repository = RaceRepository(db)

    result = repository.get_by_id(1)

    assert result is race
    db.get.assert_called_once_with(RaceModel, 1)


def test_get_by_id_returns_none_when_not_found():
    db = MagicMock()
    db.get.return_value = None

    repository = RaceRepository(db)

    result = repository.get_by_id(999)

    assert result is None
    db.get.assert_called_once_with(RaceModel, 999)


def test_list_all_returns_races():
    db = MagicMock()

    race = RaceModel(
        race_id=1,
        name="British Grand Prix",
        season=2026,
        round_number=12,
        track_id=1,
        race_date=date(2026, 7, 5),
    )

    scalars = MagicMock()
    scalars.all.return_value = [race]
    db.scalars.return_value = scalars

    repository = RaceRepository(db)

    result = repository.list_all()

    assert result == [race]
    db.scalars.assert_called_once()


def test_delete_delegates_to_session():
    db = MagicMock()
    repository = RaceRepository(db)

    race = RaceModel(
        race_id=1,
        name="British Grand Prix",
        season=2026,
        round_number=12,
        track_id=1,
        race_date=date(2026, 7, 5),
    )

    repository.delete(race)

    db.delete.assert_called_once_with(race)