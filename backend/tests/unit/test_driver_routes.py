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

        response = client.post("/api/v1/drivers", json={
            "name": "Max Verstappen",
            "nationality": "Dutch",
        })

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

        response = client.get("/api/v1/drivers/1")

        assert response.status_code == 200
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

        response = client.get("/api/v1/drivers/999")

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

        response = client.get("/api/v1/drivers")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["driver_id"] == 1

        service.list_drivers.assert_called_once_with(
            skip=0,
            limit=20,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_drivers_accepts_pagination():
    service = MagicMock()
    service.list_drivers.return_value = [make_driver()]

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/drivers?skip=20&limit=10")

        assert response.status_code == 200
        assert len(response.json()) == 1

        service.list_drivers.assert_called_once_with(
            skip=20,
            limit=10,
        )

    finally:
        app.dependency_overrides.clear()


def test_list_drivers_rejects_negative_skip():
    service = MagicMock()

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/drivers?skip=-1")

        assert response.status_code == 422
        service.list_drivers.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_list_drivers_rejects_invalid_limit():
    service = MagicMock()

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/api/v1/drivers?limit=101")

        assert response.status_code == 422
        service.list_drivers.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_delete_driver():
    service = MagicMock()
    service.delete_driver.return_value = True

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/api/v1/drivers/1")

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

        response = client.delete("/api/v1/drivers/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Driver 999 not found"

    finally:
        app.dependency_overrides.clear()


def test_delete_driver_rejects_non_positive_id():
    service = MagicMock()

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/api/v1/drivers/0")

        assert response.status_code == 422
        service.delete_driver.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_update_driver():
    service = MagicMock()
    # Return the UPDATED driver, not the original
    updated_driver = DriverModel(
        driver_id=1,
        name="Max Verstappen Updated",
        nationality="Dutch",
    )
    service.update_driver.return_value = updated_driver

    app.dependency_overrides[get_driver_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.put("/api/v1/drivers/1", json={
            "name": "Max Verstappen Updated",
            "nationality": "Dutch",
        })

        assert response.status_code == 200
        assert response.json()["name"] == "Max Verstappen Updated"

        service.update_driver.assert_called_once_with(
            driver_id=1,
            name="Max Verstappen Updated",
        )

    finally:
        app.dependency_overrides.clear()