from sqlalchemy import CheckConstraint, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TrackModel(Base):
    """SQLAlchemy model for the tracks table."""

    __tablename__ = "tracks"

    track_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    length_km: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    number_of_corners: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "length_km > 0",
            name="ck_tracks_length_km_positive",
        ),
        CheckConstraint(
            "number_of_corners >= 1",
            name="ck_tracks_number_of_corners_positive",
        ),
    )