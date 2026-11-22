from fastapi.testclient import TestClient

from app.main import app


def test_session_routes_work_end_to_end():
    client = TestClient(app)

    create_response = client.post(
        "/api/v1/sessions",
        json={
            "race_id": 1,
            "session_type": "RACE",
        },
    )

    assert create_response.status_code == 201

    created_session = create_response.json()

    assert created_session["session_id"] is not None
    assert created_session["race_id"] == 1
    assert created_session["session_type"] == "RACE"

    session_id = created_session["session_id"]

    get_response = client.get(f"/api/v1/sessions/{session_id}")

    assert get_response.status_code == 200
    assert get_response.json()["session_id"] == session_id

    list_response = client.get("/api/v1/sessions?limit=100")

    assert list_response.status_code == 200
    assert any(
        session["session_id"] == session_id
        for session in list_response.json()
    )

    delete_response = client.delete(f"/api/v1/sessions/{session_id}")

    assert delete_response.status_code == 204

    get_deleted_response = client.get(f"/api/v1/sessions/{session_id}")

    assert get_deleted_response.status_code == 404