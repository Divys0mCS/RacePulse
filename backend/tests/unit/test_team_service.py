from unittest.mock import MagicMock

import pytest

from app.database.models.team import TeamModel
from app.database.services.team_service import TeamService


def make_team() -> TeamModel:
    return TeamModel(
        team_id=1,
        name="Red Bull Racing",
        base_country="Austria",
    )


def test_create_team_creates_commits_refreshes_and_returns_team():
    db = MagicMock()
    service = TeamService(db)
    service.repository.create = MagicMock()

    result = service.create_team(
        name="Red Bull Racing",
        base_country="Austria",
    )

    assert isinstance(result, TeamModel)
    assert result.name == "Red Bull Racing"
    assert result.base_country == "Austria"

    service.repository.create.assert_called_once_with(result)
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(result)


def test_create_team_rolls_back_when_repository_fails():
    db = MagicMock()
    service = TeamService(db)

    service.repository.create = MagicMock(
        side_effect=RuntimeError("database error")
    )

    with pytest.raises(RuntimeError, match="database error"):
        service.create_team(
            name="Red Bull Racing",
            base_country="Austria",
        )

    db.rollback.assert_called_once_with()
    db.commit.assert_not_called()


def test_get_team_delegates_to_repository():
    db = MagicMock()
    service = TeamService(db)

    team = make_team()
    service.repository.get_by_id = MagicMock(return_value=team)

    result = service.get_team(1)

    assert result is team
    service.repository.get_by_id.assert_called_once_with(1)


def test_get_team_returns_none_when_not_found():
    db = MagicMock()
    service = TeamService(db)

    service.repository.get_by_id = MagicMock(return_value=None)

    result = service.get_team(999)

    assert result is None
    service.repository.get_by_id.assert_called_once_with(999)


def test_list_teams_delegates_to_repository():
    db = MagicMock()
    service = TeamService(db)

    teams = [make_team()]
    service.repository.list_all = MagicMock(return_value=teams)

    result = service.list_teams()

    assert result == teams
    service.repository.list_all.assert_called_once_with()


def test_delete_team_commits_when_team_exists():
    db = MagicMock()
    service = TeamService(db)

    team = make_team()
    service.repository.get_by_id = MagicMock(return_value=team)
    service.repository.delete = MagicMock()

    result = service.delete_team(1)

    assert result is True
    service.repository.get_by_id.assert_called_once_with(1)
    service.repository.delete.assert_called_once_with(team)
    db.commit.assert_called_once_with()


def test_delete_team_returns_false_when_team_does_not_exist():
    db = MagicMock()
    service = TeamService(db)

    service.repository.get_by_id = MagicMock(return_value=None)
    service.repository.delete = MagicMock()

    result = service.delete_team(999)

    assert result is False
    service.repository.delete.assert_not_called()
    db.commit.assert_not_called()


def test_delete_team_rolls_back_when_repository_fails():
    db = MagicMock()
    service = TeamService(db)

    team = make_team()
    service.repository.get_by_id = MagicMock(return_value=team)
    service.repository.delete = MagicMock(
        side_effect=RuntimeError("delete failed")
    )

    with pytest.raises(RuntimeError, match="delete failed"):
        service.delete_team(1)

    db.rollback.assert_called_once_with()