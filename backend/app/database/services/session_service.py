from sqlalchemy.orm import Session

from app.database.models.session import SessionModel
from app.database.repositories.race_repository import RaceRepository
from app.database.repositories.session_repository import SessionRepository


class SessionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = SessionRepository(db)
        self.race_repository = RaceRepository(db)

    def create_session(
        self,
        race_id: int,
        session_type: str,
    ) -> SessionModel:
        race = self.race_repository.get_by_id(race_id)

        if race is None:
            raise ValueError(f"Race {race_id} does not exist")

        session = SessionModel(
            race_id=race_id,
            session_type=session_type,
        )

        try:
            self.repository.create(session)
            self.db.commit()
            self.db.refresh(session)
            return session
        except Exception:
            self.db.rollback()
            raise

    def get_session(self, session_id: int) -> SessionModel | None:
        return self.repository.get_by_id(session_id)

    def get_session_by_race_and_type(
        self,
        race_id: int,
        session_type: str,
    ) -> SessionModel | None:
        return self.repository.get_by_race_and_type(
            race_id,
            session_type,
        )

    def list_sessions(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> list[SessionModel]:
        return self.repository.list_all(
            skip=skip,
            limit=limit,
        )

    def delete_session(self, session_id: int) -> bool:
        session = self.repository.get_by_id(session_id)

        if session is None:
            return False

        try:
            self.repository.delete(session)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise