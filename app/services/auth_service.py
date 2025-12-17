from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.repositories.user_repo import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @staticmethod
    def _validate_bcrypt_password(password: str) -> None:
        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes (bcrypt limitation).")

    async def register(
        self,
        session: AsyncSession,
        email: str,
        password: str,
    ) -> str:
        self._validate_bcrypt_password(password)

        existing = await self.user_repo.get_by_email(session, email)
        if existing:
            raise ValueError("Email already registered")

        hashed = hash_password(password)
        user = await self.user_repo.create(
            session,
            email=email,
            hashed_password=hashed,
        )

        return create_access_token(subject=user.email)

    async def login(
        self,
        session: AsyncSession,
        email: str,
        password: str,
    ) -> str:
        self._validate_bcrypt_password(password)

        user = await self.user_repo.get_by_email(session, email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return create_access_token(subject=user.email)
