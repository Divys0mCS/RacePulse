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

def test_sector_analysis_endpoint_returns_results():
    response = client.get("/api/v1/analysis/sector")

    assert response.status_code == 200

    data = response.json()

    assert "fastest_sector_1_seconds" in data
    assert "fastest_sector_2_seconds" in data
    assert "fastest_sector_3_seconds" in data
    assert "laps_analyzed" in data


def test_sector_analysis_endpoint_returns_valid_numbers():
    response = client.get("/api/v1/analysis/sector")

    data = response.json()

    assert data["fastest_sector_1_seconds"] > 0
    assert data["fastest_sector_2_seconds"] > 0
    assert data["fastest_sector_3_seconds"] > 0
    assert data["laps_analyzed"] > 0
    
def test_consistency_analysis_endpoint_returns_results():
    response = client.get("/api/v1/analysis/consistency")

    assert response.status_code == 200

    data = response.json()

    assert "consistency_stdev_seconds" in data
    assert "laps_analyzed" in data


def test_consistency_analysis_endpoint_returns_valid_values():
    response = client.get("/api/v1/analysis/consistency")

    data = response.json()

    assert data["consistency_stdev_seconds"] is not None
    assert data["consistency_stdev_seconds"] >= 0
    assert data["laps_analyzed"] > 0
    
def test_lap_analysis_endpoint_returns_results():
    response = client.get("/api/v1/analysis/laps")

    assert response.status_code == 200

    data = response.json()

    assert "laps_analyzed" in data
    assert "lap_times_seconds" in data
    assert "lap_time_deltas_seconds" in data


def test_lap_analysis_endpoint_returns_consistent_lengths():
    response = client.get("/api/v1/analysis/laps")

    data = response.json()

    assert data["laps_analyzed"] > 0
    assert len(data["lap_times_seconds"]) == data["laps_analyzed"]
    assert len(data["lap_time_deltas_seconds"]) == data["laps_analyzed"] - 1