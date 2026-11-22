from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.api.dependencies import get_race_service
from app.database.services.race_service import RaceService
from app.schemas.race import RaceCreate, RaceUpdate, RaceResponse


router = APIRouter(
    tags=["races"],
)


@router.post(
    "",
    response_model=RaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_race(
    race_data: RaceCreate,
    service: RaceService = Depends(get_race_service),
) -> RaceResponse:
    return service.create_race(
        name=race_data.name,
        season=race_data.season,
        round_number=race_data.round_number,
        track_id=race_data.track_id,
        race_date=race_data.race_date,
    )


@router.get(
    "",
    response_model=list[RaceResponse],
)
def list_races(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: RaceService = Depends(get_race_service),
) -> list[RaceResponse]:
    return service.list_races(
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{race_id}",
    response_model=RaceResponse,
)
def get_race(
    race_id: int = Path(gt=0),
    service: RaceService = Depends(get_race_service),
) -> RaceResponse:
    race = service.get_race(race_id)

    if race is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Race {race_id} not found",
        )

    return race


@router.put(
    "/{race_id}",
    response_model=RaceResponse,
    status_code=status.HTTP_200_OK,
)
def update_race(
    race_id: int = Path(gt=0),
    race_data: RaceUpdate = ...,
    service: RaceService = Depends(get_race_service),
) -> RaceResponse:
    race = service.update_race(race_id=race_id, name=race_data.name)

    if race is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Race {race_id} not found",
        )

    return race


@router.delete(
    "/{race_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_race(
    race_id: int = Path(gt=0),
    service: RaceService = Depends(get_race_service),
) -> None:
    deleted = service.delete_race(race_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Race {race_id} not found",
        )