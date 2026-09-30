from sqlalchemy.orm import Session

from app.database.models.track import TrackModel
from app.database.repositories.track_repository import TrackRepository


class TrackService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = TrackRepository(db)

    def create_track(
        self,
        name: str,
        country: str,
        length_km: float,
        number_of_corners: int,
    ) -> TrackModel:
        track = TrackModel(
            name=name,
            country=country,
            length_km=length_km,
            number_of_corners=number_of_corners,
        )

        try:
            self.repository.create(track)
            self.db.commit()
            self.db.refresh(track)
            return track
        except Exception:
            self.db.rollback()
            raise

    def get_track(self, track_id: int) -> TrackModel | None:
        return self.repository.get_by_id(track_id)

    def list_tracks(self) -> list[TrackModel]:
        return self.repository.list_all()

    def delete_track(self, track_id: int) -> bool:
        track = self.repository.get_by_id(track_id)

        if track is None:
            return False

        try:
            self.repository.delete(track)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise