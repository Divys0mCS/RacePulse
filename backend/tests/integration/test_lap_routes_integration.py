from fastapi.testclient import TestClient

from app.main import app


def test_lap_routes_work_end_to_end():
    client = TestClient(app)

    track_response = client.post(
        "/tracks",
        json={
            "name": "Lap API Test Circuit",
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
            "name": "Lap API Test Grand Prix",
            "season": 2026,
            "round_number": 91,
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
            "session_type": "RACE",
        },
    )

    assert session_response.status_code == 201
    session_id = session_response.json()["session_id"]

    driver_response = client.post(
        "/drivers",
        json={
            "name": "Lap API Test Driver",
            "nationality": "Test Nationality",
        },
    )

    assert driver_response.status_code == 201
    driver_id = driver_response.json()["driver_id"]

    team_response = client.post(
        "/teams",
        json={
            "name": "Lap API Test Team",
            "base_country": "Test Country",
        },
    )

    assert team_response.status_code == 201
    team_id = team_response.json()["team_id"]

    lap_response = client.post(
        "/laps",
        json={
            "session_id": session_id,
            "driver_id": driver_id,
            "team_id": team_id,
            "lap_number": 1,
            "lap_time_seconds": 92.345,
            "sector_1_time_seconds": 30.120,
            "sector_2_time_seconds": 31.210,
            "sector_3_time_seconds": 31.015,
        },
    )

    assert lap_response.status_code == 201

    created_lap = lap_response.json()

    assert created_lap["lap_id"] is not None
    assert created_lap["session_id"] == session_id
    assert created_lap["driver_id"] == driver_id
    assert created_lap["team_id"] == team_id
    assert created_lap["lap_number"] == 1

    lap_id = created_lap["lap_id"]

    get_response = client.get(f"/laps/{lap_id}")

    assert get_response.status_code == 200
    assert get_response.json()["lap_id"] == lap_id

    session_laps_response = client.get(
        f"/laps/session/{session_id}"
    )

    assert session_laps_response.status_code == 200
    assert any(
        lap["lap_id"] == lap_id
        for lap in session_laps_response.json()
    )

    composite_response = client.get(
        f"/laps/session/{session_id}/driver/{driver_id}/lap/1"
    )

    assert composite_response.status_code == 200
    assert composite_response.json()["lap_id"] == lap_id

    duplicate_response = client.post(
        "/laps",
        json={
            "session_id": session_id,
            "driver_id": driver_id,
            "team_id": team_id,
            "lap_number": 1,
            "lap_time_seconds": 93.000,
            "sector_1_time_seconds": 30.500,
            "sector_2_time_seconds": 31.500,
            "sector_3_time_seconds": 31.000,
        },
    )

    assert duplicate_response.status_code == 409

    delete_lap_response = client.delete(f"/laps/{lap_id}")

    assert delete_lap_response.status_code == 204

    get_deleted_lap_response = client.get(f"/laps/{lap_id}")

    assert get_deleted_lap_response.status_code == 404

    assert client.delete(f"/sessions/{session_id}").status_code == 204
    assert client.delete(f"/drivers/{driver_id}").status_code == 204
    assert client.delete(f"/teams/{team_id}").status_code == 204
    assert client.delete(f"/races/{race_id}").status_code == 204
    assert client.delete(f"/tracks/{track_id}").status_code == 204