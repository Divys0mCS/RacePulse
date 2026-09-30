from sqlalchemy.orm import Session

from app.database.models.team import TeamModel
from app.database.repositories.team_repository import TeamRepository


class TeamService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = TeamRepository(db)

    def create_team(
        self,
        name: str,
        base_country: str,
    ) -> TeamModel:
        team = TeamModel(
            name=name,
            base_country=base_country,
        )

        try:
            self.repository.create(team)
            self.db.commit()
            self.db.refresh(team)
            return team
        except Exception:
            self.db.rollback()
            raise

    def get_team(self, team_id: int) -> TeamModel | None:
        return self.repository.get_by_id(team_id)

    def list_teams(self) -> list[TeamModel]:
        return self.repository.list_all()

    def delete_team(self, team_id: int) -> bool:
        team = self.repository.get_by_id(team_id)

        if team is None:
            return False

        try:
            self.repository.delete(team)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise