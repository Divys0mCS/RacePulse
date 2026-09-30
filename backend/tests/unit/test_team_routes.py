from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.dependencies import get_team_service
from app.database.models.team import TeamModel
from app.main import app


def make_team() -> TeamModel:
    return TeamModel(
        team_id=1,
        name="Red Bull Racing",
        base_country="Austria",
    )


def test_create_team():
    service = MagicMock()
    service.create_team.return_value = make_team()

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/teams",
            json={
                "name": "Red Bull Racing",
                "base_country": "Austria",
            },
        )

        assert response.status_code == 201
        assert response.json() == {
            "team_id": 1,
            "name": "Red Bull Racing",
            "base_country": "Austria",
        }

        service.create_team.assert_called_once_with(
            name="Red Bull Racing",
            base_country="Austria",
        )

    finally:
        app.dependency_overrides.clear()


def test_get_team():
    service = MagicMock()
    service.get_team.return_value = make_team()

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/teams/1")

        assert response.status_code == 200
        assert response.json()["team_id"] == 1
        assert response.json()["name"] == "Red Bull Racing"

        service.get_team.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_get_team_returns_404_when_not_found():
    service = MagicMock()
    service.get_team.return_value = None

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/teams/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Team 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_list_teams():
    service = MagicMock()
    service.list_teams.return_value = [make_team()]

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/teams")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["team_id"] == 1

        service.list_teams.assert_called_once_with()

    finally:
        app.dependency_overrides.clear()


def test_delete_team():
    service = MagicMock()
    service.delete_team.return_value = True

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/teams/1")

        assert response.status_code == 204
        service.delete_team.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_delete_team_returns_404_when_not_found():
    service = MagicMock()
    service.delete_team.return_value = False

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/teams/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Team 999 not found"

    finally:
        app.dependency_overrides.clear()