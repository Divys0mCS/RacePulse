"""Integration tests for the telemetry API routes."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_telemetry_summary_returns_successful_response():
    """The telemetry summary endpoint should return HTTP 200."""

    response = client.get("/api/v1/telemetry/summary")

    assert response.status_code == 200


def test_telemetry_summary_returns_expected_structure():
    """The response should contain the expected summary fields."""

    response = client.get("/api/v1/telemetry/summary")

    assert response.status_code == 200

    data = response.json()

    assert "laps_analyzed" in data
    assert "telemetry_laps_analyzed" in data
    assert "telemetry_summaries" in data

    assert isinstance(data["laps_analyzed"], int)
    assert isinstance(data["telemetry_laps_analyzed"], int)
    assert isinstance(data["telemetry_summaries"], list)


def test_telemetry_summary_contains_valid_measurements():
    """Each returned summary should contain valid telemetry measurements."""

    response = client.get("/api/v1/telemetry/summary")

    assert response.status_code == 200

    summaries = response.json()["telemetry_summaries"]

    for summary in summaries:
        assert summary["driver_number"] > 0
        assert summary["lap_number"] >= 1
        assert summary["sample_count"] >= 1
        assert summary["maximum_speed_kph"] >= 0
        assert summary["average_speed_kph"] >= 0
        assert 0 <= summary["average_throttle_pct"] <= 100
        assert 0 <= summary["average_brake_pct"] <= 100