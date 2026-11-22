from pathlib import Path

from fastapi import APIRouter

from app.schemas.analysis import (
    PaceAnalysisResponse,
    SectorAnalysisResponse,
    ConsistencyAnalysisResponse,
    LapAnalysisResponse,
)
from app.services.analysis_service import (
    PaceAnalysisService,
    SectorAnalysisService,
    ConsistencyAnalysisService,
    LapAnalysisService,
)

router = APIRouter(
    tags=["analysis"],
)


@router.get("/pace", response_model=PaceAnalysisResponse)
def get_pace_analysis() -> dict:
    """Return pace analysis for the sample lap dataset."""

    backend_dir = Path(__file__).resolve().parents[3]
    csv_path = backend_dir / "data" / "sample" / "sample_laps.csv"

    return PaceAnalysisService().analyze(csv_path)


@router.get("/sector", response_model=SectorAnalysisResponse)
def get_sector_analysis() -> dict:
    """Return sector analysis for the sample lap dataset."""

    backend_dir = Path(__file__).resolve().parents[3]
    csv_path = backend_dir / "data" / "sample" / "sample_laps.csv"

    return SectorAnalysisService().analyze(csv_path)


@router.get("/consistency", response_model=ConsistencyAnalysisResponse)
def get_consistency_analysis() -> dict:
    """Return consistency analysis for the sample lap dataset."""

    backend_dir = Path(__file__).resolve().parents[3]
    csv_path = backend_dir / "data" / "sample" / "sample_laps.csv"

    return ConsistencyAnalysisService().analyze(csv_path)


@router.get("/laps", response_model=LapAnalysisResponse)
def get_lap_analysis() -> dict:
    """Return lap-by-lap analysis for the sample lap dataset."""

    backend_dir = Path(__file__).resolve().parents[3]
    csv_path = backend_dir / "data" / "sample" / "sample_laps.csv"

    return LapAnalysisService().analyze(csv_path)