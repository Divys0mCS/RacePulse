from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_pace_analysis_endpoint_returns_results():
    response = client.get("/api/v1/analysis/pace")

    assert response.status_code == 200

    data = response.json()

    assert "fastest_lap_seconds" in data
    assert "average_lap_seconds" in data
    assert "laps_analyzed" in data


def test_pace_analysis_endpoint_returns_valid_numbers():
    response = client.get("/api/v1/analysis/pace")

    data = response.json()

    assert isinstance(data["fastest_lap_seconds"], (int, float))
    assert isinstance(data["average_lap_seconds"], (int, float))
    assert isinstance(data["laps_analyzed"], int)

    assert data["fastest_lap_seconds"] > 0
    assert data["average_lap_seconds"] > 0
    assert data["laps_analyzed"] > 0