from datetime import date
from unittest.mock import MagicMock

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

        response = client.post(
            "/races",
            json={
                "name": "British Grand Prix",
                "season": 2026,
                "round_number": 12,
                "track_id": 5,
                "race_date": "2026-07-05",
            },
        )

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


def test_create_race_returns_404_when_track_does_not_exist():
    service = MagicMock()
    service.create_race.side_effect = ValueError(
        "Track 999 does not exist"
    )

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/races",
            json={
                "name": "British Grand Prix",
                "season": 2026,
                "round_number": 12,
                "track_id": 999,
                "race_date": "2026-07-05",
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Track 999 does not exist"

    finally:
        app.dependency_overrides.clear()


def test_create_race_rejects_blank_name():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/races",
            json={
                "name": "   ",
                "season": 2026,
                "round_number": 12,
                "track_id": 5,
                "race_date": "2026-07-05",
            },
        )

        assert response.status_code == 422
        service.create_race.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_race_rejects_name_longer_than_255_characters():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/races",
            json={
                "name": "A" * 256,
                "season": 2026,
                "round_number": 12,
                "track_id": 5,
                "race_date": "2026-07-05",
            },
        )

        assert response.status_code == 422
        service.create_race.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_race_rejects_season_before_1950():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/races",
            json={
                "name": "British Grand Prix",
                "season": 1949,
                "round_number": 12,
                "track_id": 5,
                "race_date": "2026-07-05",
            },
        )

        assert response.status_code == 422
        service.create_race.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_race_rejects_non_positive_round_number():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/races",
            json={
                "name": "British Grand Prix",
                "season": 2026,
                "round_number": 0,
                "track_id": 5,
                "race_date": "2026-07-05",
            },
        )

        assert response.status_code == 422
        service.create_race.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_race_rejects_non_positive_track_id():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/races",
            json={
                "name": "British Grand Prix",
                "season": 2026,
                "round_number": 12,
                "track_id": 0,
                "race_date": "2026-07-05",
            },
        )

        assert response.status_code == 422
        service.create_race.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_get_race():
    service = MagicMock()
    service.get_race.return_value = make_race()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/races/1")

        assert response.status_code == 200
        assert response.json()["race_id"] == 1
        assert response.json()["track_id"] == 5

        service.get_race.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_get_race_returns_404_when_not_found():
    service = MagicMock()
    service.get_race.return_value = None

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/races/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Race 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_get_race_rejects_non_positive_id():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/races/0")

        assert response.status_code == 422
        service.get_race.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_list_races():
    service = MagicMock()
    service.list_races.return_value = [make_race()]

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/races")

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

        response = client.get(
            "/races?skip=20&limit=10"
        )

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

        response = client.get(
            "/races?skip=-1"
        )

        assert response.status_code == 422
        service.list_races.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_list_races_rejects_invalid_limit():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get(
            "/races?limit=101"
        )

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

        response = client.delete("/races/1")

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

        response = client.delete("/races/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Race 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_delete_race_rejects_non_positive_id():
    service = MagicMock()

    app.dependency_overrides[get_race_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/races/0")

        assert response.status_code == 422
        service.delete_race.assert_not_called()

    finally:
        app.dependency_overrides.clear()