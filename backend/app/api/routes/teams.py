from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_team_service
from app.database.services.team_service import TeamService
from app.schemas.team import TeamCreate, TeamResponse


router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.post(
    "",
    response_model=TeamResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_team(
    team_data: TeamCreate,
    service: TeamService = Depends(get_team_service),
) -> TeamResponse:
    return service.create_team(
        name=team_data.name,
        base_country=team_data.base_country,
    )


@router.get(
    "",
    response_model=list[TeamResponse],
)
def list_teams(
    service: TeamService = Depends(get_team_service),
) -> list[TeamResponse]:
    return service.list_teams()


@router.get(
    "/{team_id}",
    response_model=TeamResponse,
)
def get_team(
    team_id: int,
    service: TeamService = Depends(get_team_service),
) -> TeamResponse:
    team = service.get_team(team_id)

    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team {team_id} not found",
        )

    return team


@router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_team(
    team_id: int,
    service: TeamService = Depends(get_team_service),
) -> None:
    deleted = service.delete_team(team_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team {team_id} not found",
        )