from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.api.dependencies import get_lap_service
from app.database.services.lap_service import LapService, LapAlreadyExistsError
from app.schemas.lap import LapCreate, LapUpdate, LapResponse


router = APIRouter(
    tags=["laps"],
)


@router.post(
    "",
    response_model=LapResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lap(
    lap_data: LapCreate,
    service: LapService = Depends(get_lap_service),
) -> LapResponse:
    try:
        return service.create_lap(
            session_id=lap_data.session_id,
            driver_id=lap_data.driver_id,
            team_id=lap_data.team_id,
            lap_number=lap_data.lap_number,
            lap_time_seconds=lap_data.lap_time_seconds,
            sector_1_time_seconds=lap_data.sector_1_time_seconds,
            sector_2_time_seconds=lap_data.sector_2_time_seconds,
            sector_3_time_seconds=lap_data.sector_3_time_seconds,
        )
    except LapAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "",
    response_model=list[LapResponse],
)
def list_laps(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: LapService = Depends(get_lap_service),
) -> list[LapResponse]:
    return service.list_laps(
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{lap_id}",
    response_model=LapResponse,
)
def get_lap(
    lap_id: int = Path(gt=0),
    service: LapService = Depends(get_lap_service),
) -> LapResponse:
    lap = service.get_lap(lap_id)

    if lap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lap {lap_id} not found",
        )

    return lap


@router.get(
    "/session/{session_id}",
    response_model=list[LapResponse],
)
def list_laps_by_session(
    session_id: int = Path(gt=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: LapService = Depends(get_lap_service),
) -> list[LapResponse]:
    return service.list_laps_by_session(session_id=session_id, skip=skip, limit=limit)


@router.get(
    "/session/{session_id}/driver/{driver_id}/lap/{lap_number}",
    response_model=LapResponse,
)
def get_lap_by_session_driver_lap(
    session_id: int = Path(gt=0),
    driver_id: int = Path(gt=0),
    lap_number: int = Path(gt=0),
    service: LapService = Depends(get_lap_service),
) -> LapResponse:
    lap = service.get_lap_by_session_driver_lap(session_id=session_id, driver_id=driver_id, lap_number=lap_number)
    if lap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lap not found for session {session_id}, driver {driver_id}, lap {lap_number}",
        )
    return lap


@router.put(
    "/{lap_id}",
    response_model=LapResponse,
    status_code=status.HTTP_200_OK,
)
def update_lap(
    lap_id: int = Path(gt=0),
    lap_data: LapUpdate = ...,
    service: LapService = Depends(get_lap_service),
) -> LapResponse:
    lap = service.update_lap(
        lap_id=lap_id,
        lap_time_seconds=lap_data.lap_time_seconds,
        sector_1_time_seconds=lap_data.sector_1_time_seconds,
        sector_2_time_seconds=lap_data.sector_2_time_seconds,
        sector_3_time_seconds=lap_data.sector_3_time_seconds,
    )

    if lap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lap {lap_id} not found",
        )

    return lap


@router.delete(
    "/{lap_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_lap(
    lap_id: int = Path(gt=0),
    service: LapService = Depends(get_lap_service),
) -> None:
    deleted = service.delete_lap(lap_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lap {lap_id} not found",
        )