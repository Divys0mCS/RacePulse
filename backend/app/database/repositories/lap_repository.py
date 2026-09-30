from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.lap import LapModel


class LapRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, lap: LapModel) -> LapModel:
        self.db.add(lap)
        self.db.flush()
        return lap

    def get_by_id(self, lap_id: int) -> LapModel | None:
        return self.db.get(LapModel, lap_id)

    def get_by_session_driver_lap(
        self,
        session_id: int,
        driver_id: int,
        lap_number: int,
    ) -> LapModel | None:
        statement = select(LapModel).where(
            LapModel.session_id == session_id,
            LapModel.driver_id == driver_id,
            LapModel.lap_number == lap_number,
        )
        return self.db.scalar(statement)

    def list_by_session(self, session_id: int) -> list[LapModel]:
        statement = (
            select(LapModel)
            .where(LapModel.session_id == session_id)
            .order_by(LapModel.lap_number)
        )
        return list(self.db.scalars(statement).all())

    def list_all(self) -> list[LapModel]:
        statement = select(LapModel).order_by(LapModel.lap_id)
        return list(self.db.scalars(statement).all())

    def delete(self, lap: LapModel) -> None:
        self.db.delete(lap)