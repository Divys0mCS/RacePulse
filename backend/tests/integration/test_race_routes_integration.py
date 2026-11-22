from fastapi.testclient import TestClient

from app.main import app


def test_race_routes_work_end_to_end():
    client = TestClient(app)

    # Create a track first
    track_create = client.post(
        "/api/v1/tracks",
        json={
            "name": "Test Track",
            "country": "Test Country",
            "length_km": 5.000,
            "number_of_corners": 10,
        },
    )
    assert track_create.status_code == 201
    track_id = track_create.json()["track_id"]

    # Create a race
    create_response = client.post(
        "/api/v1/races",
        json={
            "name": "Race API Integration Test",
            "season": 2026,
            "round_number": 99,
            "track_id": track_id,
            "race_date": "2026-09-30",
        },
    )

    assert create_response.status_code == 201

    created_race = create_response.json()

    assert created_race["race_id"] is not None
    assert created_race["name"] == "Race API Integration Test"
    assert created_race["season"] == 2026
    assert created_race["round_number"] == 99

    race_id = created_race["race_id"]

    get_response = client.get(f"/api/v1/races/{race_id}")

    assert get_response.status_code == 200
    assert get_response.json()["race_id"] == race_id
    assert get_response.json()["name"] == "Race API Integration Test"

    get_response = client.get(f"/api/v1/races/{race_id}")

    assert get_response.status_code == 200
    assert get_response.json()["race_id"] == race_id
    assert get_response.json()["name"] == "Race API Integration Test"

    delete_response = client.delete(f"/api/v1/races/{race_id}")

    assert delete_response.status_code == 204

    get_deleted_response = client.get(f"/api/v1/races/{race_id}")

    assert get_deleted_response.status_code == 404