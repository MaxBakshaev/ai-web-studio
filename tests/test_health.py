"""
Docs:
https://fastapi.tiangolo.com/advanced/async-tests/
https://www.python-httpx.org/advanced/transports/#asgi-transport
"""

from httpx import AsyncClient, ASGITransport
import pytest

from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        response = await ac.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
