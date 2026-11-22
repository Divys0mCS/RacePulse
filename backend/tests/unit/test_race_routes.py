from unittest.mock import MagicMock
from datetime import date

from fastapi.testclient import TestClient

from app.api.dependencies import get_race_service
from app.database.models.race import RaceModel
from app.main import app


def make_race() -> RaceModel:
    return RaceModel(
        race_id=1,
        name="British Grand Prix",
        season=2026,
        round_number=12,
        track_id=5,
        race_date=date(2026, 7, 5),
    )


def test_create_race():
    service = MagicMock()
    service.create_race.return_value = make_race()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/races", json={
            "name": "British Grand Prix",
            "season": 2026,
            "round_number": 12,
            "track_id": 5,
            "race_date": "2026-07-05",
        })

        assert response.status_code == 201
        assert response.json() == {
            "race_id": 1,
            "name": "British Grand Prix",
            "season": 2026,
            "round_number": 12,
            "track_id": 5,
            "race_date": "2026-07-05",
        }

        service.create_race.assert_called_once_with(
            name="British Grand Prix",
            season=2026,
            round_number=12,
            track_id=5,
            race_date=date(2026, 7, 5),
        )

    finally:
        app.dependency_overrides.clear()


def test_get_race():
    service = MagicMock()
    service.get_race.return_value = make_race()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/races/1")

        assert response.status_code == 200
        assert response.json()["name"] == "British Grand Prix"

        service.get_race.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_get_race_returns_404_when_not_found():
    service = MagicMock()
    service.get_race.return_value = None

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/races/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Race 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_list_races():
    service = MagicMock()
    service.list_races.return_value = [make_race()]

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/races")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["race_id"] == 1

        service.list_races.assert_called_once_with(
            skip=0,
            limit=20,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_races_accepts_pagination():
    service = MagicMock()
    service.list_races.return_value = [make_race()]

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/races?skip=20&limit=10")

        assert response.status_code == 200
        assert len(response.json()) == 1

        service.list_races.assert_called_once_with(
            skip=20,
            limit=10,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_races_rejects_negative_skip():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/races?skip=-1")

        assert response.status_code == 422
        service.list_races.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_list_races_rejects_invalid_limit():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/races?limit=101")

        assert response.status_code == 422
        service.list_races.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_delete_race():
    service = MagicMock()
    service.delete_race.return_value = True

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/api/v1/races/1")

        assert response.status_code == 204
        service.delete_race.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_delete_race_returns_404_when_not_found():
    service = MagicMock()
    service.delete_race.return_value = False

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/api/v1/races/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Race 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_delete_race_rejects_non_positive_id():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/api/v1/races/0")

        assert response.status_code == 422
        service.delete_race.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_update_race():
    service = MagicMock()
    updated_race = make_race()
    updated_race.name = "British Grand Prix Updated"
    service.update_race.return_value = updated_race

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.put("/api/v1/races/1", json={
            "name": "British Grand Prix Updated",
        })

        assert response.status_code == 200
        assert response.json()["name"] == "British Grand Prix Updated"

        service.update_race.assert_called_once_with(
            race_id=1,
            name="British Grand Prix Updated",
        )

    finally:
        app.dependency_overrides.clear()