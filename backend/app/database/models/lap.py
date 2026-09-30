from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.database.models.driver import DriverModel
    from app.database.models.session import SessionModel
    from app.database.models.team import TeamModel


class LapModel(Base):
    __tablename__ = "laps"

    lap_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.session_id"),
        nullable=False,
    )

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.driver_id"),
        nullable=False,
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.team_id"),
        nullable=False,
    )

    lap_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    lap_time_seconds: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    sector_1_time_seconds: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    sector_2_time_seconds: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    sector_3_time_seconds: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    session: Mapped["SessionModel"] = relationship(
        back_populates="laps",
    )

    driver: Mapped["DriverModel"] = relationship(
        back_populates="laps",
    )

    team: Mapped["TeamModel"] = relationship(
        back_populates="laps",
    )

    __table_args__ = (
        CheckConstraint(
            "lap_number >= 1",
            name="ck_laps_lap_number_positive",
        ),
        CheckConstraint(
            "lap_time_seconds > 0",
            name="ck_laps_lap_time_positive",
        ),
        CheckConstraint(
            "sector_1_time_seconds > 0",
            name="ck_laps_sector_1_positive",
        ),
        CheckConstraint(
            "sector_2_time_seconds > 0",
            name="ck_laps_sector_2_positive",
        ),
        CheckConstraint(
            "sector_3_time_seconds > 0",
            name="ck_laps_sector_3_positive",
        ),
        UniqueConstraint(
            "session_id",
            "driver_id",
            "lap_number",
            name="uq_laps_session_driver_lap",
        ),
    )