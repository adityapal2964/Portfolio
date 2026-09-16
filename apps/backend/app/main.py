from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import InvalidStateError, NotFoundError


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name)
    application.include_router(api_router, prefix="/api/v1")

    @application.exception_handler(NotFoundError)
    async def not_found_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @application.exception_handler(InvalidStateError)
    async def invalid_state_handler(_request: Request, exc: InvalidStateError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    return application


app = create_app()
