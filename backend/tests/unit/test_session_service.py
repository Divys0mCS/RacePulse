from unittest.mock import MagicMock

import pytest

from app.database.models.race import RaceModel
from app.database.models.session import SessionModel
from app.database.services.session_service import SessionService


def make_race() -> RaceModel:
    return RaceModel(
        race_id=1,
        name="British Grand Prix",
        season=2026,
        round_number=12,
        track_id=1,
    )


def make_session() -> SessionModel:
    return SessionModel(
        session_id=1,
        race_id=1,
        session_type="QUALIFYING",
    )


def test_create_session_validates_race_and_persists():
    db = MagicMock()
    service = SessionService(db)

    race = make_race()

    service.race_repository.get_by_id = MagicMock(
        return_value=race
    )
    service.repository.create = MagicMock()

    result = service.create_session(
        race_id=1,
        session_type="QUALIFYING",
    )

    assert isinstance(result, SessionModel)
    assert result.race_id == 1
    assert result.session_type == "QUALIFYING"

    service.race_repository.get_by_id.assert_called_once_with(1)
    service.repository.create.assert_called_once_with(result)
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(result)


def test_create_session_raises_when_race_does_not_exist():
    db = MagicMock()
    service = SessionService(db)

    service.race_repository.get_by_id = MagicMock(
        return_value=None
    )
    service.repository.create = MagicMock()

    with pytest.raises(ValueError, match="Race 999 does not exist"):
        service.create_session(
            race_id=999,
            session_type="RACE",
        )

    service.repository.create.assert_not_called()
    db.commit.assert_not_called()


def test_create_session_rolls_back_when_repository_fails():
    db = MagicMock()
    service = SessionService(db)

    service.race_repository.get_by_id = MagicMock(
        return_value=make_race()
    )
    service.repository.create = MagicMock(
        side_effect=RuntimeError("database error")
    )

    with pytest.raises(RuntimeError, match="database error"):
        service.create_session(
            race_id=1,
            session_type="RACE",
        )

    db.rollback.assert_called_once_with()
    db.commit.assert_not_called()


def test_get_session_delegates_to_repository():
    db = MagicMock()
    service = SessionService(db)

    session = make_session()
    service.repository.get_by_id = MagicMock(
        return_value=session
    )

    result = service.get_session(1)

    assert result is session
    service.repository.get_by_id.assert_called_once_with(1)


def test_get_session_returns_none_when_not_found():
    db = MagicMock()
    service = SessionService(db)

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.get_session(999)

    assert result is None
    service.repository.get_by_id.assert_called_once_with(999)


def test_get_session_by_race_and_type_delegates_to_repository():
    db = MagicMock()
    service = SessionService(db)

    session = make_session()
    service.repository.get_by_race_and_type = MagicMock(
        return_value=session
    )

    result = service.get_session_by_race_and_type(
        race_id=1,
        session_type="QUALIFYING",
    )

    assert result is session
    service.repository.get_by_race_and_type.assert_called_once_with(
        1,
        "QUALIFYING",
    )


def test_get_session_by_race_and_type_returns_none_when_not_found():
    db = MagicMock()
    service = SessionService(db)

    service.repository.get_by_race_and_type = MagicMock(
        return_value=None
    )

    result = service.get_session_by_race_and_type(
        race_id=1,
        session_type="RACE",
    )

    assert result is None


def test_list_sessions_delegates_pagination_to_repository():
    db = MagicMock()
    service = SessionService(db)

    sessions = [make_session()]

    service.repository.list_all = MagicMock(
        return_value=sessions
    )

    result = service.list_sessions(
        skip=20,
        limit=10,
    )

    assert result == sessions

    service.repository.list_all.assert_called_once_with(
        skip=20,
        limit=10,
    )

def test_delete_session_commits_when_session_exists():
    db = MagicMock()
    service = SessionService(db)

    session = make_session()

    service.repository.get_by_id = MagicMock(
        return_value=session
    )
    service.repository.delete = MagicMock()

    result = service.delete_session(1)

    assert result is True
    service.repository.get_by_id.assert_called_once_with(1)
    service.repository.delete.assert_called_once_with(session)
    db.commit.assert_called_once_with()


def test_delete_session_returns_false_when_session_does_not_exist():
    db = MagicMock()
    service = SessionService(db)

    service.repository.get_by_id = MagicMock(
        return_value=None
    )
    service.repository.delete = MagicMock()

    result = service.delete_session(999)

    assert result is False
    service.repository.delete.assert_not_called()
    db.commit.assert_not_called()


def test_delete_session_rolls_back_when_repository_fails():
    db = MagicMock()
    service = SessionService(db)

    session = make_session()

    service.repository.get_by_id = MagicMock(
        return_value=session
    )
    service.repository.delete = MagicMock(
        side_effect=RuntimeError("delete failed")
    )

    with pytest.raises(RuntimeError, match="delete failed"):
        service.delete_session(1)

    db.rollback.assert_called_once_with()