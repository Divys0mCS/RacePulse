from unittest.mock import MagicMock

from app.database.models.session import SessionModel
from app.database.repositories.session_repository import SessionRepository


def make_session() -> SessionModel:
    return SessionModel(
        session_id=1,
        race_id=1,
        session_type="RACE",
    )


def test_create_adds_and_flushes_session():
    db = MagicMock()
    repository = SessionRepository(db)

    session = make_session()

    result = repository.create(session)

    assert result is session
    db.add.assert_called_once_with(session)
    db.flush.assert_called_once_with()


def test_get_by_id_uses_session_get():
    db = MagicMock()

    session = make_session()

    db.get.return_value = session

    repository = SessionRepository(db)

    result = repository.get_by_id(1)

    assert result is session
    db.get.assert_called_once_with(SessionModel, 1)


def test_get_by_id_returns_none_when_not_found():
    db = MagicMock()
    db.get.return_value = None

    repository = SessionRepository(db)

    result = repository.get_by_id(999)

    assert result is None
    db.get.assert_called_once_with(SessionModel, 999)


def test_get_by_race_and_type_returns_session():
    db = MagicMock()

    session = SessionModel(
        session_id=1,
        race_id=10,
        session_type="QUALIFYING",
    )

    db.scalar.return_value = session

    repository = SessionRepository(db)

    result = repository.get_by_race_and_type(
        10,
        "QUALIFYING",
    )

    assert result is session
    db.scalar.assert_called_once()


def test_get_by_race_and_type_returns_none_when_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    repository = SessionRepository(db)

    result = repository.get_by_race_and_type(
        10,
        "RACE",
    )

    assert result is None
    db.scalar.assert_called_once()


def test_list_all_returns_sessions():
    db = MagicMock()

    session = make_session()

    scalars = MagicMock()
    scalars.all.return_value = [session]
    db.scalars.return_value = scalars

    repository = SessionRepository(db)

    result = repository.list_all()

    assert result == [session]
    db.scalars.assert_called_once()


def test_list_all_applies_pagination():
    db = MagicMock()

    session = make_session()

    scalars = MagicMock()
    scalars.all.return_value = [session]
    db.scalars.return_value = scalars

    repository = SessionRepository(db)

    result = repository.list_all(
        skip=20,
        limit=10,
    )

    assert result == [session]
    db.scalars.assert_called_once()


def test_delete_delegates_to_session():
    db = MagicMock()
    repository = SessionRepository(db)

    session = make_session()

    repository.delete(session)

    db.delete.assert_called_once_with(session)