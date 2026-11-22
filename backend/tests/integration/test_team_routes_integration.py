from fastapi.testclient import TestClient

from app.main import app


def test_team_routes_work_end_to_end():
    client = TestClient(app)

    create_response = client.post(
        "/api/v1/teams",
        json={
            "name": "Team API Integration Test",
            "base_country": "Test Country",
        },
    )

    assert create_response.status_code == 201

    created_team = create_response.json()

    assert created_team["team_id"] is not None
    assert created_team["name"] == "Team API Integration Test"
    assert created_team["base_country"] == "Test Country"

    team_id = created_team["team_id"]

    get_response = client.get(f"/api/v1/teams/{team_id}")

    assert get_response.status_code == 200
    assert get_response.json()["team_id"] == team_id
    assert get_response.json()["name"] == "Team API Integration Test"

    list_response = client.get("/api/v1/teams")

    assert list_response.status_code == 200
    assert any(
        team["team_id"] == team_id
        for team in list_response.json()
    )

    delete_response = client.delete(f"/api/v1/teams/{team_id}")

    assert delete_response.status_code == 204

    get_deleted_response = client.get(f"/api/v1/teams/{team_id}")

    assert get_deleted_response.status_code == 404
