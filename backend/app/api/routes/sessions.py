from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_session_service
from app.database.services.session_service import SessionService
from app.schemas.session import SessionCreate, SessionResponse


router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
)


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_session(
    session_data: SessionCreate,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    try:
        return service.create_session(
            race_id=session_data.race_id,
            session_type=session_data.session_type,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[SessionResponse],
)
def list_sessions(
    service: SessionService = Depends(get_session_service),
) -> list[SessionResponse]:
    return service.list_sessions()


@router.get(
    "/race/{race_id}/{session_type}",
    response_model=SessionResponse,
)
def get_session_by_race_and_type(
    race_id: int,
    session_type: str,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    session = service.get_session_by_race_and_type(
        race_id,
        session_type,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Session {session_type} for race "
                f"{race_id} not found"
            ),
        )

    return session


@router.get(
    "/{session_id}",
    response_model=SessionResponse,
)
def get_session(
    session_id: int,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    session = service.get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found",
        )

    return session


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session(
    session_id: int,
    service: SessionService = Depends(get_session_service),
) -> None:
    deleted = service.delete_session(session_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found",
        )