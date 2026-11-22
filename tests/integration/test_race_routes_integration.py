from fastapi.testclient import TestClient

from app.main import app


def test_race_routes_work_end_to_end():
    client = TestClient(app)

    create_response = client.post(
        "/api/v1/races",
        json={
            "name": "Race API Integration Test",
            "season": 2026,
            "round_number": 12,
            "track_id": 5,
            "race_date": "2026-07-05",
        },
    )

    assert create_response.status_code == 201

    created_race = create_response.json()

    assert created_race["race_id"] is not None
    assert created_race["name"] == "Race API Integration Test"
    assert created_race["season"] == 2026
    assert created_race["round_number"] == 12
    assert created_race["track_id"] == 5

    race_id = created_race["race_id"]

    get_response = client.get(f"/api/v1/races/{race_id}")

    assert get_response.status_code == 200
    assert get_response.json()["race_id"] == race_id
    assert get_response.json()["name"] == "Race API Integration Test"

    list_response = client.get("/api/v1/races?limit=100")

    assert list_response.status_code == 200
    assert any(
        race["race_id"] == race_id
        for race in list_response.json()
    )

    update_response = client.put(f"/api/v1/races/{race_id}", json={"name": "Race Updated"})

    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Race Updated"

    delete_response = client.delete(f"/api/v1/races/{race_id}")

    assert delete_response.status_code == 204

    get_deleted_response = client.get(f"/api/v1/races/{race_id}")

    assert get_deleted_response.status_code == 404