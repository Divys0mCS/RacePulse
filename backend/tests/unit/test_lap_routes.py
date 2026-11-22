from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.dependencies import get_lap_service
from app.database.models.lap import LapModel
from app.main import app


def make_lap() -> LapModel:
    return LapModel(
        lap_id=1,
        session_id=1,
        driver_id=1,
        team_id=1,
        lap_number=1,
        lap_time_seconds=95.345,
        sector_1_time_seconds=32.123,
        sector_2_time_seconds=33.456,
        sector_3_time_seconds=29.766,
    )


def test_create_lap():
    service = MagicMock()
    service.create_lap.return_value = make_lap()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 1,
            "driver_id": 1,
            "team_id": 1,
            "lap_number": 1,
            "lap_time_seconds": 95.345,
            "sector_1_time_seconds": 32.123,
            "sector_2_time_seconds": 33.456,
            "sector_3_time_seconds": 29.766,
        })

        assert response.status_code == 201
        assert response.json() == {
            "lap_id": 1,
            "session_id": 1,
            "driver_id": 1,
            "team_id": 1,
            "lap_number": 1,
            "lap_time_seconds": 95.345,
            "sector_1_time_seconds": 32.123,
            "sector_2_time_seconds": 33.456,
            "sector_3_time_seconds": 29.766,
        }

        service.create_lap.assert_called_once_with(
            session_id=1,
            driver_id=1,
            team_id=1,
            lap_number=1,
            lap_time_seconds=95.345,
            sector_1_time_seconds=32.123,
            sector_2_time_seconds=33.456,
            sector_3_time_seconds=29.766,
        )

    finally:
        app.dependency_overrides.clear()


def test_create_lap_raises_422_on_invalid_dependency():
    """Bad input / unexpected dependency failure should return 422."""
    from app.database.services.lap_service import InvalidSessionError
    service = MagicMock()
    service.create_lap.side_effect = InvalidSessionError("Session 999 does not exist")    app.dependency_overrides[get_lap_service] = lambda: service    try:
        client = TestClient(app)
        response = client.post("/api/v1/laps", json={
            "session_id": 999,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 1,
            "lap_time_seconds": 90.0,
            "sector_1_time_seconds": 30.0,
            "sector_2_time_seconds": 30.0,
            "sector_3_time_seconds": 30.0,
        })
        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()


def test_create_lap_raises_409_on_duplicate():
    """Duplicate lap should return 409 Conflict."""
    from app.database.services.lap_service import LapAlreadyExistsError
    service = MagicMock()
    service.create_lap.side_effect = LapAlreadyExistsError("Lap already exists for this session, driver, and lap number")    app.dependency_overrides[get_lap_service] = lambda: service    try:
        client = TestClient(app)
        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })
        assert response.status_code == 409    finally:
        app.dependency_overrides.clear()


def test_create_lap_raises_500_on_unexpected_service_error():
    """Unexpected service/database exception should return 500."""
    service = MagicMock()
    service.create_lap.side_effect = RuntimeError("Unexpected database failure")    app.dependency_overrides[get_lap_service] = lambda: service    try:
        client = TestClient(app)
        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })
        assert response.status_code == 500    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_non_positive_session_id():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 0,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_non_positive_driver_id():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 0,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_non_positive_team_id():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 0,
            "lap_number": 5,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_non_positive_lap_number():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 0,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_invalid_lap_time():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": 0,
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_invalid_sector_1_time():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": 0,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_invalid_sector_2_time():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 0,
            "sector_3_time_seconds": 31.015,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_invalid_sector_3_time():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 0,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_nan_lap_time():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": "NaN",
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_infinite_lap_time():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": "Infinity",
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_create_lap_rejects_nan_sector_time():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post("/api/v1/laps", json={
            "session_id": 10,
            "driver_id": 20,
            "team_id": 30,
            "lap_number": 5,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": "NaN",
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        })

        assert response.status_code == 422
        service.create_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_get_lap():
    service = MagicMock()
    service.get_lap.return_value = make_lap()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/1")

        assert response.status_code == 200
        assert response.json()["lap_id"] == 1
        assert response.json()["lap_number"] == 1

        service.get_lap.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_get_lap_returns_404_when_not_found():
    service = MagicMock()
    service.get_lap.return_value = None

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Lap 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_get_lap_rejects_non_positive_id():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/0")

        assert response.status_code == 422
        service.get_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_list_laps():
    service = MagicMock()
    service.list_laps.return_value = [make_lap()]

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["lap_id"] == 1

        service.list_laps.assert_called_once_with(
            skip=0,
            limit=20,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_laps_accepts_pagination():
    service = MagicMock()
    service.list_laps.return_value = [make_lap()]

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps?skip=20&limit=10")

        assert response.status_code == 200
        assert len(response.json()) == 1

        service.list_laps.assert_called_once_with(
            skip=20,
            limit=10,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_laps_rejects_negative_skip():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps?skip=-1")

        assert response.status_code == 422
        service.list_laps.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_list_laps_rejects_invalid_limit():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps?limit=101")

        assert response.status_code == 422
        service.list_laps.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_list_laps_by_session():
    service = MagicMock()
    service.list_laps_by_session.return_value = [make_lap()]

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/session/1")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["lap_id"] == 1

        service.list_laps_by_session.assert_called_once_with(
            session_id=1,
            skip=0,
            limit=20,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_laps_by_session_accepts_pagination():
    service = MagicMock()
    service.list_laps_by_session.return_value = [make_lap()]

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/session/1?skip=20&limit=10")

        assert response.status_code == 200
        assert len(response.json()) == 1

        service.list_laps_by_session.assert_called_once_with(
            session_id=1,
            skip=20,
            limit=10,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_laps_by_session_rejects_non_positive_session_id():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/session/0")

        assert response.status_code == 422
        service.list_laps_by_session.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_list_laps_by_session_rejects_negative_skip():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/session/1?skip=-1")

        assert response.status_code == 422
        service.list_laps_by_session.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_list_laps_by_session_rejects_invalid_limit():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/session/1?limit=101")

        assert response.status_code == 422
        service.list_laps_by_session.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_get_lap_by_session_driver_lap():
    service = MagicMock()
    service.get_lap_by_session_driver_lap.return_value = make_lap()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/session/1/driver/1/lap/1")

        assert response.status_code == 200
        assert response.json()["lap_id"] == 1

        service.get_lap_by_session_driver_lap.assert_called_once_with(
            session_id=1,
            driver_id=1,
            lap_number=1,
        )

    finally:
        app.dependency_overrides.clear()


def test_get_lap_by_session_driver_lap_returns_404():
    service = MagicMock()
    service.get_lap_by_session_driver_lap.return_value = None

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/session/1/driver/1/lap/999")

        assert response.status_code == 404

    finally:
        app.dependency_overrides.clear()


def test_get_lap_by_session_driver_lap_rejects_non_positive_session_id():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/session/0/driver/1/lap/5")

        assert response.status_code == 422
        service.get_lap_by_session_driver_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_get_lap_by_session_driver_lap_rejects_non_positive_driver_id():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/session/1/driver/0/lap/5")

        assert response.status_code == 422
        service.get_lap_by_session_driver_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_get_lap_by_session_driver_lap_rejects_invalid_lap_number():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/laps/session/1/driver/1/lap/0")

        assert response.status_code == 422
        service.get_lap_by_session_driver_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_delete_lap():
    service = MagicMock()
    service.delete_lap.return_value = True

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/api/v1/laps/1")

        assert response.status_code == 204
        service.delete_lap.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_delete_lap_returns_404_when_not_found():
    service = MagicMock()
    service.delete_lap.return_value = False

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/api/v1/laps/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Lap 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_delete_lap_rejects_non_positive_id():
    service = MagicMock()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/api/v1/laps/0")

        assert response.status_code == 422
        service.delete_lap.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_update_lap():
    service = MagicMock()
    service.update_lap.return_value = make_lap()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.put("/api/v1/laps/1", json={
            "lap_time_seconds": 93.123,
            "sector_1_time_seconds": 31.5,
            "sector_2_time_seconds": 33.0,
            "sector_3_time_seconds": 28.6,
        })

        assert response.status_code == 200
        assert response.json()["lap_time_seconds"] == 95.345

        service.update_lap.assert_called_once_with(
            lap_id=1,
            lap_time_seconds=93.123,
            sector_1_time_seconds=31.5,
            sector_2_time_seconds=33.0,
            sector_3_time_seconds=28.6,
        )

    finally:
        app.dependency_overrides.clear()


def test_update_lap_partial():
    service = MagicMock()
    service.update_lap.return_value = make_lap()

    app.dependency_overrides[get_lap_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.put("/api/v1/laps/1", json={
            "lap_time_seconds": 92.999,
        })

        assert response.status_code == 200
        assert response.json()["lap_time_seconds"] == 95.345

        service.update_lap.assert_called_once_with(
            lap_id=1,
            lap_time_seconds=92.999,
            sector_1_time_seconds=None,
            sector_2_time_seconds=None,
            sector_3_time_seconds=None,
        )

    finally:
        app.dependency_overrides.clear()
