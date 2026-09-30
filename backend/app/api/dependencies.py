from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.services.race_service import RaceService
from app.database.services.track_service import TrackService


def get_track_service(
    db: Session = Depends(get_db),
) -> TrackService:
    return TrackService(db)


def get_race_service(
    db: Session = Depends(get_db),
) -> RaceService:
    return RaceService(db)