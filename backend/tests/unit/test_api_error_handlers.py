from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.error_handlers import (
    file_not_found_handler,
    generic_exception_handler,
)


def create_test_app() -> FastAPI:
    app = FastAPI()

    app.add_exception_handler(
        FileNotFoundError,
        file_not_found_handler,
    )
    app.add_exception_handler(
        Exception,
        generic_exception_handler,
    )

    @app.get("/missing")
    def missing_file() -> None:
        raise FileNotFoundError("sample.csv")

    @app.get("/broken")
    def broken_endpoint() -> None:
        raise RuntimeError("database exploded")

    return app


def test_file_not_found_returns_404() -> None:
    client = TestClient(create_test_app())

    response = client.get("/missing")

    assert response.status_code == 404
    assert response.json() == {"detail": "sample.csv"}


def test_unexpected_exception_returns_500() -> None:
    client = TestClient(
        create_test_app(),
        raise_server_exceptions=False,
    )

    response = client.get("/broken")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}