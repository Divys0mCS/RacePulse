from fastapi.testclient import TestClient

from app.main import app


def test_session_routes_work_end_to_end():
    client = TestClient(app)

    # Create a track first
    track_response = client.post(
        "/api/v1/tracks",
        json={
            "name": "Session API Test Circuit",
            "country": "Test Country",
            "length_km": 5.900,
            "number_of_corners": 18,
        },
    )
    assert track_response.status_code == 201
    track_id = track_response.json()["track_id"]

    # Create a race
    race_response = client.post(
        "/api/v1/races",
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

    # Create a session
    session_response = client.post(
        "/api/v1/sessions",
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

    # Get session
    get_response = client.get(f"/api/v1/sessions/{session_id}")

    assert get_response.status_code == 200
    assert get_response.json()["session_id"] == session_id

    # List sessions
    list_response = client.get("/api/v1/sessions")

    assert list_response.status_code == 200
    assert any(
        session["session_id"] == session_id
        for session in list_response.json()
    )

    # Delete session
    delete_response = client.delete(f"/api/v1/sessions/{session_id}")

    assert delete_response.status_code == 204

    # Verify deleted
    get_deleted_response = client.get(f"/api/v1/sessions/{session_id}")

    assert get_deleted_response.status_code == 404

    # Delete race
    delete_race_response = client.delete(f"/api/v1/races/{race_id}")
    assert delete_race_response.status_code == 204

    # Delete track
    delete_track_response = client.delete(f"/api/v1/tracks/{track_id}")
    assert delete_track_response.status_code == 204
