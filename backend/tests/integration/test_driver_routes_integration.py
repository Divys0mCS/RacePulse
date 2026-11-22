from fastapi.testclient import TestClient

from app.main import app


def test_driver_routes_work_end_to_end():
    client = TestClient(app)

    create_response = client.post(
        "/api/v1/drivers",
        json={
            "name": "Driver API Integration Test",
            "nationality": "Test Nationality",
        },
    )

    assert create_response.status_code == 201

    created_driver = create_response.json()

    assert created_driver["driver_id"] is not None
    assert created_driver["name"] == "Driver API Integration Test"
    assert created_driver["nationality"] == "Test Nationality"

    driver_id = created_driver["driver_id"]

    get_response = client.get(f"/api/v1/drivers/{driver_id}")

    assert get_response.status_code == 200
    assert get_response.json()["driver_id"] == driver_id
    assert get_response.json()["name"] == "Driver API Integration Test"

    list_response = client.get("/api/v1/drivers?limit=100")

    assert list_response.status_code == 200
    assert any(
        driver["driver_id"] == driver_id
        for driver in list_response.json()
    )

    delete_response = client.delete(f"/api/v1/drivers/{driver_id}")

    assert delete_response.status_code == 204

    get_deleted_response = client.get(f"/api/v1/drivers/{driver_id}")

    assert get_deleted_response.status_code == 404