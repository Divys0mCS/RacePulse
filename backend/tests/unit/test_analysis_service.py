from pathlib import Path

from app.services.analysis_service import (
    PaceAnalysisService,
    SectorAnalysisService,
    ConsistencyAnalysisService,
    LapAnalysisService,
)

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
def test_sector_analysis_service_returns_expected_result():
    csv_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "sample"
        / "sample_laps.csv"
    )

    result = SectorAnalysisService().analyze(csv_path)

    assert set(result) == {
        "fastest_sector_1_seconds",
        "fastest_sector_2_seconds",
        "fastest_sector_3_seconds",
        "laps_analyzed",
    }

    assert result["fastest_sector_1_seconds"] > 0
    assert result["fastest_sector_2_seconds"] > 0
    assert result["fastest_sector_3_seconds"] > 0
    assert result["laps_analyzed"] > 0

def test_consistency_analysis_service_returns_expected_result():
    csv_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "sample"
        / "sample_laps.csv"
    )

    result = ConsistencyAnalysisService().analyze(csv_path)

    assert set(result) == {
        "consistency_stdev_seconds",
        "laps_analyzed",
    }

    assert result["consistency_stdev_seconds"] is not None
    assert result["consistency_stdev_seconds"] >= 0
    assert result["laps_analyzed"] > 0

def test_lap_analysis_service_returns_expected_result():
    csv_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "sample"
        / "sample_laps.csv"
    )

    result = LapAnalysisService().analyze(csv_path)

    assert set(result) == {
        "laps_analyzed",
        "lap_times_seconds",
        "lap_time_deltas_seconds",
    }

    assert result["laps_analyzed"] > 0
    assert len(result["lap_times_seconds"]) == result["laps_analyzed"]
    assert len(result["lap_time_deltas_seconds"]) == result["laps_analyzed"] - 1