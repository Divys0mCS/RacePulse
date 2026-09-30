from unittest.mock import MagicMock

from app.database.models.team import TeamModel
from app.database.repositories.team_repository import TeamRepository


def test_create_adds_and_flushes_team():
    db = MagicMock()
    repository = TeamRepository(db)

    team = TeamModel(
        name="Red Bull Racing",
        base_country="Austria",
    )

    result = repository.create(team)

    assert result is team
    db.add.assert_called_once_with(team)
    db.flush.assert_called_once_with()


def test_get_by_id_uses_session_get():
    db = MagicMock()

    team = TeamModel(
        team_id=1,
        name="Red Bull Racing",
        base_country="Austria",
    )

    db.get.return_value = team

    repository = TeamRepository(db)

    result = repository.get_by_id(1)

    assert result is team
    db.get.assert_called_once_with(TeamModel, 1)


def test_get_by_id_returns_none_when_not_found():
    db = MagicMock()
    db.get.return_value = None

    repository = TeamRepository(db)

    result = repository.get_by_id(999)

    assert result is None
    db.get.assert_called_once_with(TeamModel, 999)


def test_list_all_returns_teams():
    db = MagicMock()

    team = TeamModel(
        team_id=1,
        name="Red Bull Racing",
        base_country="Austria",
    )

    scalars = MagicMock()
    scalars.all.return_value = [team]
    db.scalars.return_value = scalars

    repository = TeamRepository(db)

    result = repository.list_all()

    assert result == [team]
    db.scalars.assert_called_once()


def test_delete_delegates_to_session():
    db = MagicMock()
    repository = TeamRepository(db)

    team = TeamModel(
        team_id=1,
        name="Red Bull Racing",
        base_country="Austria",
    )

    repository.delete(team)

    db.delete.assert_called_once_with(team)