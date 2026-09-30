from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.team import TeamModel


class TeamRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, team: TeamModel) -> TeamModel:
        self.db.add(team)
        self.db.flush()
        return team

    def get_by_id(self, team_id: int) -> TeamModel | None:
        return self.db.get(TeamModel, team_id)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> list[TeamModel]:
        statement = (
            select(TeamModel)
            .order_by(TeamModel.team_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def delete(self, team: TeamModel) -> None:
        self.db.delete(team)