"""Tests for the telemetry service."""

from unittest.mock import MagicMock, patch

from app.services.telemetry_service import TelemetryService


@patch("app.services.telemetry_service.TelemetryLoader")
@patch("app.services.telemetry_service.CSVLoader")
def test_analyze_returns_telemetry_summaries(
    mock_csv_loader,
    mock_telemetry_loader,
    tmp_path,
):
    lap = MagicMock()
    lap.driver.name = "Max Verstappen"
    lap.driver.number = 1
    lap.lap_number = 5
    lap.lap_time_seconds = 91.5

    mock_csv_loader.return_value.load.return_value = [lap]

    telemetry = MagicMock()
    telemetry.samples = [
        MagicMock(speed_kph=200.0, throttle_pct=100.0, brake_pct=0.0),
        MagicMock(speed_kph=250.0, throttle_pct=80.0, brake_pct=20.0),
    ]
    telemetry.lap = lap
    telemetry.max_speed_kph.return_value = 250.0

    mock_telemetry_loader.return_value.load.return_value = [telemetry]

    result = TelemetryService().analyze(
        tmp_path / "laps.csv",
        tmp_path / "telemetry.csv",
    )

    assert result["laps_analyzed"] == 1
    assert result["telemetry_laps_analyzed"] == 1

    summary = result["telemetry_summaries"][0]

    assert summary["driver_name"] == "Max Verstappen"
    assert summary["driver_number"] == 1
    assert summary["lap_number"] == 5
    assert summary["lap_time_seconds"] == 91.5
    assert summary["sample_count"] == 2
    assert summary["maximum_speed_kph"] == 250.0
    assert summary["average_speed_kph"] == 225.0
    assert summary["average_throttle_pct"] == 90.0
    assert summary["average_brake_pct"] == 10.0


@patch("app.services.telemetry_service.CSVLoader")
def test_analyze_handles_empty_lap_data(mock_csv_loader, tmp_path):
    mock_csv_loader.return_value.load.return_value = []

    result = TelemetryService().analyze(
        tmp_path / "laps.csv",
        tmp_path / "telemetry.csv",
    )

    assert result == {
        "laps_analyzed": 0,
        "telemetry_laps_analyzed": 0,
        "telemetry_summaries": [],
    }