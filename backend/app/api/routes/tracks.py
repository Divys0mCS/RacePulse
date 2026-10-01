from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.api.dependencies import get_track_service
from app.database.services.track_service import TrackService
from app.schemas.track import TrackCreate, TrackResponse


router = APIRouter(
    prefix="/tracks",
    tags=["tracks"],
)


@router.post(
    "",
    response_model=TrackResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_track(
    track_data: TrackCreate,
    service: TrackService = Depends(get_track_service),
) -> TrackResponse:
    return service.create_track(
        name=track_data.name,
        country=track_data.country,
        length_km=track_data.length_km,
        number_of_corners=track_data.number_of_corners,
    )


@router.get(
    "",
    response_model=list[TrackResponse],
)
def list_tracks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: TrackService = Depends(get_track_service),
) -> list[TrackResponse]:
    return service.list_tracks(
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{track_id}",
    response_model=TrackResponse,
)
def get_track(
    track_id: int = Path(gt=0),
    service: TrackService = Depends(get_track_service),
) -> TrackResponse:
    track = service.get_track(track_id)

    if track is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Track {track_id} not found",
        )

    return track


@router.delete(
    "/{track_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_track(
    track_id: int = Path(gt=0),
    service: TrackService = Depends(get_track_service),
) -> None:
    deleted = service.delete_track(track_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Track {track_id} not found",
        )