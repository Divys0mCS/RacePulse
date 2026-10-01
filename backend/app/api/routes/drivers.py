from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.api.dependencies import get_driver_service
from app.database.services.driver_service import DriverService
from app.schemas.driver import DriverCreate, DriverResponse


router = APIRouter(
    prefix="/drivers",
    tags=["drivers"],
)


@router.post(
    "",
    response_model=DriverResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_driver(
    driver_data: DriverCreate,
    service: DriverService = Depends(get_driver_service),
) -> DriverResponse:
    return service.create_driver(
        name=driver_data.name,
        nationality=driver_data.nationality,
    )


@router.get(
    "",
    response_model=list[DriverResponse],
)
def list_drivers(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: DriverService = Depends(get_driver_service),
) -> list[DriverResponse]:
    return service.list_drivers(
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{driver_id}",
    response_model=DriverResponse,
)
def get_driver(
    driver_id: int = Path(gt=0),
    service: DriverService = Depends(get_driver_service),
) -> DriverResponse:
    driver = service.get_driver(driver_id)

    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver {driver_id} not found",
        )

    return driver


@router.delete(
    "/{driver_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_driver(
    driver_id: int = Path(gt=0),
    service: DriverService = Depends(get_driver_service),
) -> None:
    deleted = service.delete_driver(driver_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver {driver_id} not found",
        )