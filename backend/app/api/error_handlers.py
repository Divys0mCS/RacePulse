from fastapi import Request
from fastapi.responses import JSONResponse


async def file_not_found_handler(
    request: Request,
    exc: FileNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )