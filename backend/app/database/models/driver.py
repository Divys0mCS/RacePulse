from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.models.lap import LapModel
class DriverModel(Base):
    __tablename__ = "drivers"

    driver_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    nationality: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    laps: Mapped[list["LapModel"]] = relationship(
        back_populates="driver",
    )