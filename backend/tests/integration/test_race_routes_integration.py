from fastapi.testclient import TestClient

from app.main import app


def test_race_routes_work_end_to_end():
    client = TestClient(app)

    track_response = client.post(
        "/tracks",
        json={
            "name": "Race API Integration Test Circuit",
            "country": "Test Country",
            "length_km": 5.950,
            "number_of_corners": 18,
        },
    )

    assert track_response.status_code == 201

    track_id = track_response.json()["track_id"]

    race_response = client.post(
        "/races",
        json={
            "name": "Race API Integration Test",
            "season": 2026,
            "round_number": 93,
            "track_id": track_id,
            "race_date": "2026-09-30",
        },
    )

    assert race_response.status_code == 201

    created_race = race_response.json()

    assert created_race["race_id"] is not None
    assert created_race["track_id"] == track_id

    race_id = created_race["race_id"]

    get_response = client.get(f"/races/{race_id}")

    assert get_response.status_code == 200
    assert get_response.json()["race_id"] == race_id
    assert get_response.json()["track_id"] == track_id

    list_response = client.get("/races")

    assert list_response.status_code == 200
    assert any(
        race["race_id"] == race_id
        for race in list_response.json()
    )

    delete_race_response = client.delete(f"/races/{race_id}")

    assert delete_race_response.status_code == 204

    get_deleted_race_response = client.get(f"/races/{race_id}")

    assert get_deleted_race_response.status_code == 404

    delete_track_response = client.delete(f"/tracks/{track_id}")

    assert delete_track_response.status_code == 204