from fastapi.testclient import TestClient

from app.main import app


def test_session_routes_work_end_to_end():
    client = TestClient(app)

    track_response = client.post(
        "/tracks",
        json={
            "name": "Session API Test Circuit",
            "country": "Test Country",
            "length_km": 5.900,
            "number_of_corners": 18,
        },
    )

    assert track_response.status_code == 201
    track_id = track_response.json()["track_id"]

    race_response = client.post(
        "/races",
        json={
            "name": "Session API Test Grand Prix",
            "season": 2026,
            "round_number": 92,
            "track_id": track_id,
            "race_date": "2026-09-30",
        },
    )

    assert race_response.status_code == 201
    race_id = race_response.json()["race_id"]

    session_response = client.post(
        "/sessions",
        json={
            "race_id": race_id,
            "session_type": "QUALIFYING",
        },
    )

    assert session_response.status_code == 201

    created_session = session_response.json()

    assert created_session["session_id"] is not None
    assert created_session["race_id"] == race_id
    assert created_session["session_type"] == "QUALIFYING"

    session_id = created_session["session_id"]

    get_response = client.get(
        f"/sessions/{session_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["session_id"] == session_id

    race_type_response = client.get(
        f"/sessions/race/{race_id}/QUALIFYING"
    )

    assert race_type_response.status_code == 200
    assert race_type_response.json()["session_id"] == session_id

    list_response = client.get("/sessions")

    assert list_response.status_code == 200
    assert any(
        session["session_id"] == session_id
        for session in list_response.json()
    )

    delete_response = client.delete(
        f"/sessions/{session_id}"
    )

    assert delete_response.status_code == 204

    get_deleted_response = client.get(
        f"/sessions/{session_id}"
    )

    assert get_deleted_response.status_code == 404

    delete_race_response = client.delete(f"/races/{race_id}")
    assert delete_race_response.status_code == 204

    delete_track_response = client.delete(f"/tracks/{track_id}")
    assert delete_track_response.status_code == 204