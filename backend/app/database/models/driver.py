from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


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