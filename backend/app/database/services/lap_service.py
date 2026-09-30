from sqlalchemy.orm import Session

from app.database.models.lap import LapModel
from app.database.repositories.driver_repository import DriverRepository
from app.database.repositories.lap_repository import LapRepository
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.team_repository import TeamRepository


class LapAlreadyExistsError(ValueError):
    """Raised when a lap already exists for a session, driver, and lap number."""


class LapService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = LapRepository(db)
        self.session_repository = SessionRepository(db)
        self.driver_repository = DriverRepository(db)
        self.team_repository = TeamRepository(db)

    def create_lap(
        self,
        session_id: int,
        driver_id: int,
        team_id: int,
        lap_number: int,
        lap_time_seconds: float,
        sector_1_time_seconds: float,
        sector_2_time_seconds: float,
        sector_3_time_seconds: float,
    ) -> LapModel:
        session = self.session_repository.get_by_id(session_id)

        if session is None:
            raise ValueError(f"Session {session_id} does not exist")

        driver = self.driver_repository.get_by_id(driver_id)

        if driver is None:
            raise ValueError(f"Driver {driver_id} does not exist")

        team = self.team_repository.get_by_id(team_id)

        if team is None:
            raise ValueError(f"Team {team_id} does not exist")

        existing_lap = self.repository.get_by_session_driver_lap(
            session_id,
            driver_id,
            lap_number,
        )

        if existing_lap is not None:
            raise LapAlreadyExistsError(
                "Lap already exists for this session, driver, and lap number"
            )

        lap = LapModel(
            session_id=session_id,
            driver_id=driver_id,
            team_id=team_id,
            lap_number=lap_number,
            lap_time_seconds=lap_time_seconds,
            sector_1_time_seconds=sector_1_time_seconds,
            sector_2_time_seconds=sector_2_time_seconds,
            sector_3_time_seconds=sector_3_time_seconds,
        )

        try:
            self.repository.create(lap)
            self.db.commit()
            self.db.refresh(lap)
            return lap
        except Exception:
            self.db.rollback()
            raise

    def get_lap(self, lap_id: int) -> LapModel | None:
        return self.repository.get_by_id(lap_id)

    def get_lap_by_session_driver_lap(
        self,
        session_id: int,
        driver_id: int,
        lap_number: int,
    ) -> LapModel | None:
        return self.repository.get_by_session_driver_lap(
            session_id,
            driver_id,
            lap_number,
        )

    def list_laps_by_session(
        self,
        session_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[LapModel]:
        return self.repository.list_by_session(
            session_id,
            skip=skip,
            limit=limit,
        )

    def list_laps(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> list[LapModel]:
        return self.repository.list_all(
            skip=skip,
            limit=limit,
        )

    def delete_lap(self, lap_id: int) -> bool:
        lap = self.repository.get_by_id(lap_id)

        if lap is None:
            return False

        try:
            self.repository.delete(lap)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise