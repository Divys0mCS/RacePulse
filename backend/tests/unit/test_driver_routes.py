from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.dependencies import get_driver_service
from app.database.models.driver import DriverModel
from app.main import app


def make_driver() -> DriverModel:
    return DriverModel(
        driver_id=1,
        name="Max Verstappen",
        nationality="Dutch",
    )


def test_create_driver():
    service = MagicMock()
    service.create_driver.return_value = make_driver()

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/drivers",
            json={
                "name": "Max Verstappen",
                "nationality": "Dutch",
            },
        )

        assert response.status_code == 201
        assert response.json() == {
            "driver_id": 1,
            "name": "Max Verstappen",
            "nationality": "Dutch",
        }

        service.create_driver.assert_called_once_with(
            name="Max Verstappen",
            nationality="Dutch",
        )

    finally:
        app.dependency_overrides.clear()


def test_get_driver():
    service = MagicMock()
    service.get_driver.return_value = make_driver()

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/drivers/1")

        assert response.status_code == 200
        assert response.json()["driver_id"] == 1
        assert response.json()["name"] == "Max Verstappen"

        service.get_driver.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_get_driver_returns_404_when_not_found():
    service = MagicMock()
    service.get_driver.return_value = None

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/drivers/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Driver 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_list_drivers():
    service = MagicMock()
    service.list_drivers.return_value = [make_driver()]

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/drivers")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["driver_id"] == 1

        service.list_drivers.assert_called_once_with()

    finally:
        app.dependency_overrides.clear()


def test_delete_driver():
    service = MagicMock()
    service.delete_driver.return_value = True

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/drivers/1")

        assert response.status_code == 204
        service.delete_driver.assert_called_once_with(1)

    finally:
        app.dependency_overrides.clear()


def test_delete_driver_returns_404_when_not_found():
    service = MagicMock()
    service.delete_driver.return_value = False

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/drivers/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Driver 999 not found"

    finally:
        app.dependency_overrides.clear()