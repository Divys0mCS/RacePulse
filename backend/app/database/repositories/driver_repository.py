from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.driver import DriverModel


class DriverRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, driver: DriverModel) -> DriverModel:
        self.db.add(driver)
        self.db.flush()
        return driver

    def get_by_id(self, driver_id: int) -> DriverModel | None:
        return self.db.get(DriverModel, driver_id)

    def list_all(self) -> list[DriverModel]:
        statement = select(DriverModel).order_by(DriverModel.driver_id)
        return list(self.db.scalars(statement).all())

    def delete(self, driver: DriverModel) -> None:
        self.db.delete(driver)