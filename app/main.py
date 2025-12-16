"""Docs: https://fastapi.tiangolo.com/#create-it"""

from fastapi import FastAPI

from .core.config import settings
from .core.logging import setup_logging
from .api.v1 import health


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
    )
    app.include_router(health.router)

    return app


app = create_app()

# uvicorn app.main:app --reload
