"""Docs: https://fastapi.tiangolo.com/#create-it"""

from .api.v1.health import router as health_router
from .api.v1.auth import router as auth_router
from .api.v1.users import router as users_router

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

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)

# uvicorn app.main:app --reload
