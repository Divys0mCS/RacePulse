import os
import pytest

from app.database.connection import engine, SessionLocal

# Ensure tests use a dedicated test database, not the development database
database_url = os.getenv("DATABASE_URL", "")
test_database_url = os.getenv("TEST_DATABASE_URL", "")

# Refuse to run if DATABASE_URL points to development database 
# without a TEST_DATABASE_URL override
_dev_indicators = ["localhost", ".db"]
if any(indicator in database_url.lower() for indicator in _dev_indicators) and not test_database_url:
    raise RuntimeError(
        f"DATABASE_URL points to development database: {database_url}. "
        f"Set TEST_DATABASE_URL to a dedicated test database."
    )

@pytest.fixture(autouse=True, scope="function")
def isolate_database():
    """Isolate each test function with a transaction that is rolled back after the test."""
    connection = engine.connect()
    transaction = connection.begin()
    
    # Bind the session to the connection using the test DB URL
    session = SessionLocal(bind=connection)
    
    yield session
    
    # Roll back the transaction to undo all changes
    session.close()
    transaction.rollback()
    connection.close()