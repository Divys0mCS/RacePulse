from unittest.mock import MagicMock, patch

from app.database.dependencies import get_db


def test_get_db_provides_session_and_closes_it() -> None:
    mock_session = MagicMock()

    with patch(
        "app.database.dependencies.SessionLocal",
        return_value=mock_session,
    ):
        generator = get_db()

        db = next(generator)

        assert db is mock_session

        try:
            next(generator)
        except StopIteration:
            pass

        mock_session.close.assert_called_once()