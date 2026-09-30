from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.dependencies import get_session_service
from app.database.models.session import SessionModel
from app.main import app


def make_session() -> SessionModel:
    return SessionModel(
        session_id=1,
        race_id=10,
        session_type="QUALIFYING",
    )


def test_create_session():
    service = MagicMock()
    service.create_session.return_value = make_session()

    app.dependency_overrides[get_session_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/sessions",
            json={
                "race_id": 10,
                "session_type": "QUALIFYING",
            },
        )

        assert response.status_code == 201
        assert response.json() == {
            "session_id": 1,
            "race_id": 10,
            "session_type": "QUALIFYING",
        }

        service.create_session.assert_called_once_with(
            race_id=10,
            session_type="QUALIFYING",
        )

    finally:
        app.dependency_overrides.clear()


def test_create_session_returns_404_when_race_does_not_exist():
    service = MagicMock()
    service.create_session.side_effect = ValueError(
        "Race 999 does not exist"
    )

    app.dependency_overrides[get_session_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/sessions",
            json={
                "race_id": 999,
                "session_type": "RACE",
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Race 999 does not exist"

    finally:
        app.dependency_overrides.clear()


def test_create_session_rejects_invalid_session_type():
    service = MagicMock()

    app.dependency_overrides[get_session_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/sessions",
            json={
                "race_id": 10,
                "session_type": "INVALID",
            },
        )

        assert response.status_code == 422
        service.create_session.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_get_session():
    service = MagicMock()
    service.get_session.return_value = make_session()

    app.dependency_overrides[get_session_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/sessions/1")

        assert response.status_code == 200
        assert response.json()["session_id"] == 1
        assert response.json()["race_id"] == 10

        service.get_session.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_get_session_returns_404_when_not_found():
    service = MagicMock()
    service.get_session.return_value = None

    app.dependency_overrides[get_session_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/sessions/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Session 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_get_session_by_race_and_type():
    service = MagicMock()
    service.get_session_by_race_and_type.return_value = make_session()

    app.dependency_overrides[get_session_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get(
            "/sessions/race/10/QUALIFYING"
        )

        assert response.status_code == 200
        assert response.json()["session_id"] == 1

        service.get_session_by_race_and_type.assert_called_once_with(
            10,
            "QUALIFYING",
        )

    finally:
        app.dependency_overrides.clear()


def test_get_session_by_race_and_type_returns_404_when_not_found():
    service = MagicMock()
    service.get_session_by_race_and_type.return_value = None

    app.dependency_overrides[get_session_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get(
            "/sessions/race/10/RACE"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == (
            "Session RACE for race 10 not found"
        )

    finally:
        app.dependency_overrides.clear()


def test_list_sessions():
    service = MagicMock()
    service.list_sessions.return_value = [make_session()]

    app.dependency_overrides[get_session_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/sessions")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["session_id"] == 1

        service.list_sessions.assert_called_once_with()

    finally:
        app.dependency_overrides.clear()


def test_delete_session():
    service = MagicMock()
    service.delete_session.return_value = True

    app.dependency_overrides[get_session_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/sessions/1")

        assert response.status_code == 204
        service.delete_session.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_delete_session_returns_404_when_not_found():
    service = MagicMock()
    service.delete_session.return_value = False

    app.dependency_overrides[get_session_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/sessions/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Session 999 not found"

    finally:
        app.dependency_overrides.clear()