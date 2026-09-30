from sqlalchemy.orm import Session

from app.database.models.driver import DriverModel
from app.database.repositories.driver_repository import DriverRepository


class DriverService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = DriverRepository(db)

    def create_driver(
        self,
        name: str,
        nationality: str,
    ) -> DriverModel:
        driver = DriverModel(
            name=name,
            nationality=nationality,
        )

        try:
            self.repository.create(driver)
            self.db.commit()
            self.db.refresh(driver)
            return driver
        except Exception:
            self.db.rollback()
            raise

    def get_driver(self, driver_id: int) -> DriverModel | None:
        return self.repository.get_by_id(driver_id)

    def list_drivers(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> list[DriverModel]:
        return self.repository.list_all(
            skip=skip,
            limit=limit,
        )

    def delete_driver(self, driver_id: int) -> bool:
        driver = self.repository.get_by_id(driver_id)

        if driver is None:
            return False

        try:
            self.repository.delete(driver)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise