from pathlib import Path

from app.services.analysis_service import PaceAnalysisService


def test_pace_analysis_service_returns_json_ready_result():
    csv_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "sample"
        / "sample_laps.csv"
    )

    result = PaceAnalysisService().analyze(csv_path)

    assert set(result) == {
        "fastest_lap_seconds",
        "average_lap_seconds",
        "laps_analyzed",
    }

    assert result["fastest_lap_seconds"] > 0
    assert result["average_lap_seconds"] > 0
    assert result["laps_analyzed"] > 0


def test_pace_analysis_service_returns_numeric_values():
    csv_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "sample"
        / "sample_laps.csv"
    )

    result = PaceAnalysisService().analyze(csv_path)

    assert isinstance(result["fastest_lap_seconds"], (int, float))
    assert isinstance(result["average_lap_seconds"], (int, float))
    assert isinstance(result["laps_analyzed"], int)