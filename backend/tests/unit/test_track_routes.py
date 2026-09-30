from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.dependencies import get_track_service
from app.database.models.track import TrackModel
from app.main import app


def make_track() -> TrackModel:
    return TrackModel(
        track_id=1,
        name="Silverstone",
        country="United Kingdom",
        length_km=5.891,
        number_of_corners=18,
    )


def test_create_track():
    service = MagicMock()
    service.create_track.return_value = make_track()

    app.dependency_overrides[get_track_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/tracks",
            json={
                "name": "Silverstone",
                "country": "United Kingdom",
                "length_km": 5.891,
                "number_of_corners": 18,
            },
        )

        assert response.status_code == 201
        assert response.json() == {
            "track_id": 1,
            "name": "Silverstone",
            "country": "United Kingdom",
            "length_km": 5.891,
            "number_of_corners": 18,
        }

        service.create_track.assert_called_once_with(
            name="Silverstone",
            country="United Kingdom",
            length_km=5.891,
            number_of_corners=18,
        )

    finally:
        app.dependency_overrides.clear()


def test_get_track():
    service = MagicMock()
    service.get_track.return_value = make_track()

    app.dependency_overrides[get_track_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/tracks/1")

        assert response.status_code == 200
        assert response.json()["name"] == "Silverstone"
        service.get_track.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_get_track_returns_404_when_not_found():
    service = MagicMock()
    service.get_track.return_value = None

    app.dependency_overrides[get_track_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/tracks/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Track 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_list_tracks():
    service = MagicMock()
    service.list_tracks.return_value = [make_track()]

    app.dependency_overrides[get_track_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/tracks")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["track_id"] == 1
        service.list_tracks.assert_called_once_with()

    finally:
        app.dependency_overrides.clear()


def test_delete_track():
    service = MagicMock()
    service.delete_track.return_value = True

    app.dependency_overrides[get_track_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/tracks/1")

        assert response.status_code == 204
        service.delete_track.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_delete_track_returns_404_when_not_found():
    service = MagicMock()
    service.delete_track.return_value = False

    app.dependency_overrides[get_track_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/tracks/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Track 999 not found"

    finally:
        app.dependency_overrides.clear()