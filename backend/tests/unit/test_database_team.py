from sqlalchemy import inspect

from app.database.base import Base
from app.database.models.team import TeamModel


def test_team_model_uses_teams_table() -> None:
    assert TeamModel.__tablename__ == "teams"


def test_team_model_inherits_from_base() -> None:
    assert issubclass(TeamModel, Base)


def test_team_model_has_expected_columns() -> None:
    columns = set(TeamModel.__table__.columns.keys())

    assert columns == {
        "team_id",
        "name",
        "base_country",
    }


def test_team_id_is_primary_key() -> None:
    primary_keys = {
        column.name
        for column in inspect(TeamModel).primary_key
    }

    assert primary_keys == {"team_id"}


def test_team_columns_are_non_nullable() -> None:
    for column in TeamModel.__table__.columns:
        assert column.nullable is False