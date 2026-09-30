from fastapi import FastAPI
from app.api.routes.tracks import router as tracks_router
from app.api.routes.races import router as races_router

from app.api.error_handlers import (
    file_not_found_handler,
    generic_exception_handler,
)
from app.api.routes.analysis import router as analysis_router


app = FastAPI(
    title="RacePulse API",
    version="0.1.0",
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


app.include_router(analysis_router)
app.include_router(tracks_router)
app.include_router(races_router)