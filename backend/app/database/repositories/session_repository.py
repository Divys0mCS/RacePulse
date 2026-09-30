from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.session import SessionModel


class SessionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, session: SessionModel) -> SessionModel:
        self.db.add(session)
        self.db.flush()
        return session

    def get_by_id(self, session_id: int) -> SessionModel | None:
        return self.db.get(SessionModel, session_id)

    def get_by_race_and_type(
        self,
        race_id: int,
        session_type: str,
    ) -> SessionModel | None:
        statement = select(SessionModel).where(
            SessionModel.race_id == race_id,
            SessionModel.session_type == session_type,
        )
        return self.db.scalar(statement)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> list[SessionModel]:
        statement = (
            select(SessionModel)
            .order_by(SessionModel.session_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def delete(self, session: SessionModel) -> None:
        self.db.delete(session)