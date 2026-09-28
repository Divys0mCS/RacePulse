from pathlib import Path

from fastapi import APIRouter

from analytics.analysis.pace_analysis import PaceAnalyzer
from analytics.loaders.csv_loader import CSVLoader

router = APIRouter(
    prefix="/api/v1/analysis",
    tags=["analysis"],
)


@router.get("/pace")
def get_pace_analysis() -> dict:
    """Return pace analysis for the sample lap dataset."""

    backend_dir = Path(__file__).resolve().parents[3]
    csv_path = backend_dir / "data" / "sample" / "sample_laps.csv"

    laps = CSVLoader().load(csv_path)
    result = PaceAnalyzer().analyze(laps)

    return {
        "fastest_lap_seconds": result["fastest_lap"].lap_time_seconds,
        "average_lap_seconds": result["average_lap_time_seconds"],
        "laps_analyzed": result["laps_analyzed"],
    }