from app.database.connection import SessionLocal
from app.database.models.driver import DriverModel
from app.database.repositories.driver_repository import DriverRepository


def test_driver_repository_persists_driver():
    db = SessionLocal()
    
    try:
        repository = DriverRepository(db)

        driver = DriverModel(
            name="Integration Test Driver",
            nationality="Test Nationality",
        )

        created_driver = repository.create(driver)
        db.commit()

        assert created_driver.driver_id is not None

        fetched_driver = repository.get_by_id(created_driver.driver_id)

        assert fetched_driver is not None
        assert fetched_driver.driver_id == created_driver.driver_id
        assert fetched_driver.name == "Integration Test Driver"
        assert fetched_driver.nationality == "Test Nationality"

        # Use limit=200 to ensure we capture the newly created driver
        # (database may have many drivers from previous test runs)
        drivers = list(repository.list_all(limit=200))

        assert any(
            existing.driver_id == created_driver.driver_id
            for existing in drivers
        )

        repository.delete(fetched_driver)
        db.commit()

        assert repository.get_by_id(created_driver.driver_id) is None

    finally:
        db.close()