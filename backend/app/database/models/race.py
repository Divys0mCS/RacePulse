from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.models.track import TrackModel


class RaceModel(Base):
    """SQLAlchemy model for the races table."""

    __tablename__ = "races"

    race_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    season: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    round_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    track_id: Mapped[int] = mapped_column(
        ForeignKey("tracks.track_id"),
        nullable=False,
    )

    race_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    track: Mapped[TrackModel] = relationship(
        back_populates="races",
    )

    __table_args__ = (
        CheckConstraint(
            "season >= 1950",
            name="ck_races_season_valid",
        ),
        CheckConstraint(
            "round_number >= 1",
            name="ck_races_round_number_positive",
        ),
    )