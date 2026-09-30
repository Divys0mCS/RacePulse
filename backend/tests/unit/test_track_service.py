from unittest.mock import MagicMock

from app.database.models.track import TrackModel
from app.database.services.track_service import TrackService


def test_create_track_creates_commits_refreshes_and_returns_track():
    db = MagicMock()
    service = TrackService(db)

    result = service.create_track(
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )

    assert isinstance(result, TrackModel)
    assert result.name == "Silverstone"
    assert result.country == "United Kingdom"
    assert result.length_km == 5.891
    assert result.number_of_corners == 18

    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(result)


def test_create_track_rolls_back_when_repository_fails():
    db = MagicMock()
    service = TrackService(db)

    service.repository.create = MagicMock(
        side_effect=RuntimeError("database error")
    )

    try:
        service.create_track(
            name="Silverstone",
            country="United Kingdom",
            length_km=5.891,
            number_of_corners=18,
        )
    except RuntimeError as exc:
        assert str(exc) == "database error"
    else:
        raise AssertionError("RuntimeError was not raised")

    db.rollback.assert_called_once_with()
    db.commit.assert_not_called()


def test_get_track_delegates_to_repository():
    db = MagicMock()
    service = TrackService(db)

    track = TrackModel(
        track_id=1,
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )

    service.repository.get_by_id = MagicMock(return_value=track)

    result = service.get_track(1)

    assert result is track
    service.repository.get_by_id.assert_called_once_with(1)


def test_get_track_returns_none_when_not_found():
    db = MagicMock()
    service = TrackService(db)

    service.repository.get_by_id = MagicMock(return_value=None)

    result = service.get_track(999)

    assert result is None
    service.repository.get_by_id.assert_called_once_with(999)


def test_list_tracks_delegates_pagination_to_repository():
    db = MagicMock()
    service = TrackService(db)

    tracks = [
        TrackModel(
            track_id=1,
            name="Silverstone",
            country="United Kingdom",
            length_km=5.891,
            number_of_corners=18,
        )
    ]

    service.repository.list_all = MagicMock(
        return_value=tracks
    )

    result = service.list_tracks(
        skip=20,
        limit=10,
    )

    assert result == tracks

    service.repository.list_all.assert_called_once_with(
        skip=20,
        limit=10,
    )


def test_delete_track_commits_when_track_exists():
    db = MagicMock()
    service = TrackService(db)

    track = TrackModel(
        track_id=1,
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )

    service.repository.get_by_id = MagicMock(return_value=track)
    service.repository.delete = MagicMock()

    result = service.delete_track(1)

    assert result is True
    service.repository.get_by_id.assert_called_once_with(1)
    service.repository.delete.assert_called_once_with(track)
    db.commit.assert_called_once_with()


def test_delete_track_returns_false_when_track_does_not_exist():
    db = MagicMock()
    service = TrackService(db)

    service.repository.get_by_id = MagicMock(return_value=None)
    service.repository.delete = MagicMock()

    result = service.delete_track(999)

    assert result is False
    service.repository.delete.assert_not_called()
    db.commit.assert_not_called()


def test_delete_track_rolls_back_when_repository_fails():
    db = MagicMock()
    service = TrackService(db)

    track = TrackModel(
        track_id=1,
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )

    service.repository.get_by_id = MagicMock(return_value=track)
    service.repository.delete = MagicMock(
        side_effect=RuntimeError("delete failed")
    )

    try:
        service.delete_track(1)
    except RuntimeError as exc:
        assert str(exc) == "delete failed"
    else:
        raise AssertionError("RuntimeError was not raised")

    db.rollback.assert_called_once_with()