from datetime import date
from unittest.mock import MagicMock

import pytest

from app.database.models.race import RaceModel
from app.database.models.track import TrackModel
from app.database.services.race_service import RaceService


def make_track() -> TrackModel:
    return TrackModel(
        track_id=1,
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )


def make_race() -> RaceModel:
    return RaceModel(
        race_id=1,
        name="British Grand Prix",
        season=2026,
        round_number=12,
        track_id=1,
        race_date=date(2026, 7, 5),
    )


def test_create_race_validates_track_and_persists():
    db = MagicMock()
    service = RaceService(db)

    service.track_repository.get_by_id = MagicMock(
        return_value=make_track()
    )
    service.repository.create = MagicMock()

    result = service.create_race(
        name="British Grand Prix",
        season=2026,
        round_number=12,
        track_id=1,
        race_date=date(2026, 7, 5),
    )

    assert isinstance(result, RaceModel)
    assert result.name == "British Grand Prix"
    assert result.track_id == 1

    service.track_repository.get_by_id.assert_called_once_with(1)
    service.repository.create.assert_called_once_with(result)
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(result)


def test_create_race_raises_when_track_does_not_exist():
    db = MagicMock()
    service = RaceService(db)

    service.track_repository.get_by_id = MagicMock(
        return_value=None
    )
    service.repository.create = MagicMock()

    with pytest.raises(ValueError, match="Track 999 does not exist"):
        service.create_race(
            name="British Grand Prix",
            season=2026,
            round_number=12,
            track_id=999,
            race_date=date(2026, 7, 5),
        )

    service.repository.create.assert_not_called()
    db.commit.assert_not_called()


def test_create_race_rolls_back_when_repository_fails():
    db = MagicMock()
    service = RaceService(db)

    service.track_repository.get_by_id = MagicMock(
        return_value=make_track()
    )
    service.repository.create = MagicMock(
        side_effect=RuntimeError("database error")
    )

    with pytest.raises(RuntimeError, match="database error"):
        service.create_race(
            name="British Grand Prix",
            season=2026,
            round_number=12,
            track_id=1,
            race_date=date(2026, 7, 5),
        )

    db.rollback.assert_called_once_with()
    db.commit.assert_not_called()


def test_get_race_delegates_to_repository():
    db = MagicMock()
    service = RaceService(db)

    race = make_race()
    service.repository.get_by_id = MagicMock(
        return_value=race
    )

    result = service.get_race(1)

    assert result is race
    service.repository.get_by_id.assert_called_once_with(1)


def test_get_race_returns_none_when_not_found():
    db = MagicMock()
    service = RaceService(db)

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.get_race(999)

    assert result is None
    service.repository.get_by_id.assert_called_once_with(999)


def test_list_races_delegates_to_repository():
    db = MagicMock()
    service = RaceService(db)

    races = [make_race()]
    service.repository.list_all = MagicMock(
        return_value=races
    )

    result = service.list_races(
        skip=20,
        limit=10,
    )

    assert result == races

    service.repository.list_all.assert_called_once_with(
        skip=20,
        limit=10,
    )


def test_delete_race_commits_when_race_exists():
    db = MagicMock()
    service = RaceService(db)

    race = make_race()
    service.repository.get_by_id = MagicMock(
        return_value=race
    )
    service.repository.delete = MagicMock()

    result = service.delete_race(1)

    assert result is True
    service.repository.get_by_id.assert_called_once_with(1)
    service.repository.delete.assert_called_once_with(race)
    db.commit.assert_called_once_with()


def test_delete_race_returns_false_when_race_does_not_exist():
    db = MagicMock()
    service = RaceService(db)

    service.repository.get_by_id = MagicMock(
        return_value=None
    )
    service.repository.delete = MagicMock()

    result = service.delete_race(999)

    assert result is False
    service.repository.delete.assert_not_called()
    db.commit.assert_not_called()


def test_delete_race_rolls_back_when_repository_fails():
    db = MagicMock()
    service = RaceService(db)

    race = make_race()
    service.repository.get_by_id = MagicMock(
        return_value=race
    )
    service.repository.delete = MagicMock(
        side_effect=RuntimeError("delete failed")
    )

    with pytest.raises(RuntimeError, match="delete failed"):
        service.delete_race(1)

    db.rollback.assert_called_once_with()
    
def test_list_races_delegates_pagination_to_repository():
    db = MagicMock()
    service = RaceService(db)

    races = [make_race()]

    service.repository.list_all = MagicMock(
        return_value=races
    )

    result = service.list_races(
        skip=20,
        limit=10,
    )

    assert result == races

    service.repository.list_all.assert_called_once_with(
        skip=20,
        limit=10,
    )