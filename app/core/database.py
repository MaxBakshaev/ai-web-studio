"""Docs: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html"""

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from .config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # логирование SQL при DEBUG=true
    future=True,
)


# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Зависимость для FastAPI (получение сессии в запросе)
async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
