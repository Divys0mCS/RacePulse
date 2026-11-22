from fastapi.testclient import TestClient

from app.main import app


def test_track_routes_work_end_to_end():
    client = TestClient(app)

    create_response = client.post(
        "/api/v1/tracks",
        json={
            "name": "Track API Integration Test",
            "country": "Test Country",
            "length_km": 5.950,
            "number_of_corners": 18,
        },
    )

    assert create_response.status_code == 201

    created_track = create_response.json()

    assert created_track["track_id"] is not None
    assert created_track["name"] == "Track API Integration Test"
    assert created_track["country"] == "Test Country"
    assert created_track["length_km"] == 5.950
    assert created_track["number_of_corners"] == 18

    track_id = created_track["track_id"]

    get_response = client.get(f"/api/v1/tracks/{track_id}")

    assert get_response.status_code == 200
    assert get_response.json()["track_id"] == track_id
    assert get_response.json()["name"] == "Track API Integration Test"

    list_response = client.get("/api/v1/tracks?limit=100")

    assert list_response.status_code == 200
    assert any(
        track["track_id"] == track_id
        for track in list_response.json()
    )

    delete_response = client.delete(f"/api/v1/tracks/{track_id}")

    assert delete_response.status_code == 204

    get_deleted_response = client.get(f"/api/v1/tracks/{track_id}")

    assert get_deleted_response.status_code == 404