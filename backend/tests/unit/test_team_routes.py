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


def test_create_team_rejects_blank_name():
    service = MagicMock()

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/teams",
            json={
                "name": "   ",
                "base_country": "Austria",
            },
        )

        assert response.status_code == 422
        service.create_team.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_team_rejects_name_longer_than_255_characters():
    service = MagicMock()

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/teams",
            json={
                "name": "A" * 256,
                "base_country": "Austria",
            },
        )

        assert response.status_code == 422
        service.create_team.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_team_rejects_blank_base_country():
    service = MagicMock()

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/teams",
            json={
                "name": "Red Bull Racing",
                "base_country": "   ",
            },
        )

        assert response.status_code == 422
        service.create_team.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_team_rejects_base_country_longer_than_100_characters():
    service = MagicMock()

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/teams",
            json={
                "name": "Red Bull Racing",
                "base_country": "A" * 101,
            },
        )

        assert response.status_code == 422
        service.create_team.assert_not_called()

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


def test_get_team_rejects_non_positive_id():
    service = MagicMock()

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/teams/0")

        assert response.status_code == 422
        service.get_team.assert_not_called()

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

        service.list_teams.assert_called_once_with(
            skip=0,
            limit=20,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_teams_accepts_pagination():
    service = MagicMock()
    service.list_teams.return_value = [make_team()]

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get(
            "/teams?skip=20&limit=10"
        )

        assert response.status_code == 200
        assert len(response.json()) == 1

        service.list_teams.assert_called_once_with(
            skip=20,
            limit=10,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_teams_rejects_negative_skip():
    service = MagicMock()

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get(
            "/teams?skip=-1"
        )

        assert response.status_code == 422
        service.list_teams.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_list_teams_rejects_invalid_limit():
    service = MagicMock()

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get(
            "/teams?limit=101"
        )

        assert response.status_code == 422
        service.list_teams.assert_not_called()

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


def test_delete_team_rejects_non_positive_id():
    service = MagicMock()

    app.dependency_overrides[get_team_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/teams/0")

        assert response.status_code == 422
        service.delete_team.assert_not_called()

    finally:
        app.dependency_overrides.clear()