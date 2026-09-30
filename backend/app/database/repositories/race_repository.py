from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.race import RaceModel


class RaceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, race: RaceModel) -> RaceModel:
        self.db.add(race)
        self.db.flush()
        return race

    def get_by_id(self, race_id: int) -> RaceModel | None:
        return self.db.get(RaceModel, race_id)

    def list_all(self) -> list[RaceModel]:
        statement = select(RaceModel).order_by(RaceModel.race_id)
        return list(self.db.scalars(statement).all())

    def delete(self, race: RaceModel) -> None:
        self.db.delete(race)