from app.database.connection import SessionLocal
from app.database.services.driver_service import DriverService


def test_driver_service_creates_reads_lists_and_deletes_driver():
    db = SessionLocal()

    try:
        service = DriverService(db)

        created_driver = service.create_driver(
            name="Driver Service Integration Test",
            nationality="Test Nationality",
        )

        assert created_driver.driver_id is not None

        fetched_driver = service.get_driver(created_driver.driver_id)

        assert fetched_driver is not None
        assert fetched_driver.name == "Driver Service Integration Test"
        assert fetched_driver.nationality == "Test Nationality"

        drivers = service.list_drivers()

        assert any(
            driver.driver_id == created_driver.driver_id
            for driver in drivers
        )

        assert service.delete_driver(created_driver.driver_id) is True
        assert service.get_driver(created_driver.driver_id) is None

    finally:
        db.rollback()
        db.close()