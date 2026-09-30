from unittest.mock import MagicMock

from app.database.models.track import TrackModel
from app.database.repositories.track_repository import TrackRepository


def test_create_adds_and_flushes_track():
    db = MagicMock()
    repository = TrackRepository(db)

    track = TrackModel(
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )

    result = repository.create(track)

    assert result is track
    db.add.assert_called_once_with(track)
    db.flush.assert_called_once_with()


def test_get_by_id_uses_session_get():
    db = MagicMock()

    track = TrackModel(
        track_id=1,
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )

    db.get.return_value = track

    repository = TrackRepository(db)

    result = repository.get_by_id(1)

    assert result is track
    db.get.assert_called_once_with(TrackModel, 1)


def test_get_by_id_returns_none_when_not_found():
    db = MagicMock()
    db.get.return_value = None

    repository = TrackRepository(db)

    result = repository.get_by_id(999)

    assert result is None
    db.get.assert_called_once_with(TrackModel, 999)


def test_list_all_returns_tracks():
    db = MagicMock()

    track = TrackModel(
        track_id=1,
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )

    scalars = MagicMock()
    scalars.all.return_value = [track]
    db.scalars.return_value = scalars

    repository = TrackRepository(db)

    result = repository.list_all()

    assert result == [track]
    db.scalars.assert_called_once()


def test_delete_delegates_to_session():
    db = MagicMock()
    repository = TrackRepository(db)

    track = TrackModel(
        track_id=1,
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )

    repository.delete(track)

    db.delete.assert_called_once_with(track)