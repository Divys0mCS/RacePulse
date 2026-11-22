"""API routes for historical telemetry analysis."""

from pathlib import Path

from fastapi import APIRouter

from app.schemas.telemetry import TelemetryAnalysisResponse
from app.services.telemetry_service import TelemetryService

router = APIRouter(
    tags=["telemetry"],
)




@router.get(
    "/summary",
    response_model=TelemetryAnalysisResponse,
)
def get_telemetry_summary() -> dict:
    """Return telemetry summaries for the bundled sample data."""

    backend_dir = Path(__file__).resolve().parents[3]

    laps_csv_path = (
        backend_dir / "data" / "sample" / "sample_laps.csv"
    )
    telemetry_csv_path = (
        backend_dir / "data" / "sample" / "sample_telemetry.csv"
    )

    service = TelemetryService()

    return service.analyze(
        laps_csv_path=laps_csv_path,
        telemetry_csv_path=telemetry_csv_path,
    )