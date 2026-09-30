from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.database.models.race import RaceModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.models.lap import LapModel
class SessionModel(Base):
    __tablename__ = "sessions"

    session_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    race_id: Mapped[int] = mapped_column(
        ForeignKey("races.race_id"),
        nullable=False,
    )

    session_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    race: Mapped[RaceModel] = relationship(
        back_populates="sessions",
    )

    __table_args__ = (
        CheckConstraint(
            """
            session_type IN (
                'FP1',
                'FP2',
                'FP3',
                'SPRINT_QUALIFYING',
                'SPRINT',
                'QUALIFYING',
                'RACE'
            )
            """,
            name="ck_sessions_session_type_valid",
        ),
        UniqueConstraint(
            "race_id",
            "session_type",
            name="uq_sessions_race_session_type",
        ),
    )
    laps: Mapped[list["LapModel"]] = relationship(
        back_populates="session",
    )