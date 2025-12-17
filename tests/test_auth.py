import uuid
import pytest


def _email() -> str:
    return f"u{uuid.uuid4().hex[:10]}@example.com"


@pytest.mark.asyncio
async def test_register_and_me(client):
    email = _email()
    password = "strongpass123"

    r = await client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    assert token

    r2 = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r2.status_code == 200, r2.text
    assert r2.json()["email"] == email


@pytest.mark.asyncio
async def test_login_success(client):
    email = _email()
    password = "strongpass123"

    await client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    r = await client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    assert r.status_code == 200, r.text
    assert "access_token" in r.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    email = _email()
    password = "strongpass123"

    await client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    r = await client.post(
        "/auth/login",
        json={"email": email, "password": "WRONG_PASS"},
    )

    assert r.status_code == 401, r.text


@pytest.mark.asyncio
async def test_me_without_token(client):
    r = await client.get("/users/me")
    assert r.status_code == 403 or r.status_code == 401


@pytest.mark.asyncio
async def test_password_too_long_bytes(client):
    email = _email()
    # 80 ASCII символов = 80 bytes > 72 bytes
    long_password = "a" * 80

    r = await client.post(
        "/auth/register",
        json={"email": email, "password": long_password},
    )
    assert r.status_code == 422, r.text
    assert "at most 72 characters" in r.text
