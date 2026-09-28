from pathlib import Path

from fastapi import APIRouter

from app.services.analysis_service import PaceAnalysisService


router = APIRouter(
    prefix="/api/v1/analysis",
    tags=["analysis"],
)


@router.get("/pace")
def get_pace_analysis() -> dict:
    """Return pace analysis for the sample lap dataset."""

    backend_dir = Path(__file__).resolve().parents[3]
    csv_path = backend_dir / "data" / "sample" / "sample_laps.csv"

    return PaceAnalysisService().analyze(csv_path)