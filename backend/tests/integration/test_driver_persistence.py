from app.database.connection import SessionLocal
from app.database.models.driver import DriverModel


def test_driver_can_be_inserted_and_read_back() -> None:
    session = SessionLocal()

    try:
        driver = DriverModel(
            name="Max Verstappen",
            nationality="Dutch",
        )

        session.add(driver)
        session.commit()
        session.refresh(driver)

        assert driver.driver_id is not None

        saved_driver = session.get(DriverModel, driver.driver_id)

        assert saved_driver is not None
        assert saved_driver.name == "Max Verstappen"
        assert saved_driver.nationality == "Dutch"

        session.delete(saved_driver)
        session.commit()

    finally:
        session.close()