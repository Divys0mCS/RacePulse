from datetime import date

from sqlalchemy.orm import Session

from app.database.models.race import RaceModel
from app.database.repositories.race_repository import RaceRepository
from app.database.repositories.track_repository import TrackRepository


class RaceService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = RaceRepository(db)
        self.track_repository = TrackRepository(db)

    def create_race(
        self,
        name: str,
        season: int,
        round_number: int,
        track_id: int,
        race_date: date,
    ) -> RaceModel:
        track = self.track_repository.get_by_id(track_id)

        if track is None:
            raise ValueError(f"Track {track_id} does not exist")

        race = RaceModel(
            name=name,
            season=season,
            round_number=round_number,
            track_id=track_id,
            race_date=race_date,
        )

        try:
            self.repository.create(race)
            self.db.commit()
            self.db.expire_all()  # Refresh session to see newly committed data
            self.db.refresh(race)
            return race
        except Exception:
            self.db.rollback()
            raise

    def get_race(self, race_id: int) -> RaceModel | None:
        return self.repository.get_by_id(race_id)

    def list_races(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> list[RaceModel]:
        return self.repository.list_all(
            skip=skip,
            limit=limit,
        )

    def update_race(self, race_id: int, name: str) -> RaceModel | None:
        race = self.repository.get_by_id(race_id)

        if race is None:
            return None

        race.name = name

        try:
            self.db.commit()
            self.db.refresh(race)
            return race
        except Exception:
            self.db.rollback()
            raise

    def delete_race(self, race_id: int) -> bool:
        race = self.repository.get_by_id(race_id)

        if race is None:
            return False

        try:
            self.repository.delete(race)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise