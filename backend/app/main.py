from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.error_handlers import (
    file_not_found_handler,
    generic_exception_handler,
)
from app.api.routes.analysis import router as analysis_router
from app.api.routes.drivers import router as drivers_router
from app.api.routes.laps import router as laps_router
from app.api.routes.races import router as races_router
from app.api.routes.sessions import router as sessions_router
from app.api.routes.teams import router as teams_router
from app.api.routes.tracks import router as tracks_router
from app.api.routes.telemetry import router as telemetry_router
from app.config.settings import settings
from app.database.dependencies import get_db

app = FastAPI(
    title="RacePulse API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.add_exception_handler(
    FileNotFoundError,
    file_not_found_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def readiness_check(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    return {"status": "ready", "database": db_status}


app.include_router(analysis_router, prefix="/api/v1/analysis")
app.include_router(tracks_router, prefix="/api/v1/tracks")
app.include_router(races_router, prefix="/api/v1/races")
app.include_router(drivers_router, prefix="/api/v1/drivers")
app.include_router(teams_router, prefix="/api/v1/teams")
app.include_router(sessions_router, prefix="/api/v1/sessions")
app.include_router(laps_router, prefix="/api/v1/laps")
app.include_router(telemetry_router, prefix="/api/v1/telemetry")
