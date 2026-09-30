from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.track import TrackModel


class TrackRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, track: TrackModel) -> TrackModel:
        self.db.add(track)
        self.db.flush()
        return track

    def get_by_id(self, track_id: int) -> TrackModel | None:
        return self.db.get(TrackModel, track_id)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> list[TrackModel]:
        statement = (
        select(TrackModel)
        .order_by(TrackModel.track_id)
        .offset(skip)
        .limit(limit)
    )
        return list(self.db.scalars(statement).all())

    def delete(self, track: TrackModel) -> None:
        self.db.delete(track)