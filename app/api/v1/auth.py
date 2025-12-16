from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.auth import RegisterIn, LoginIn, TokenOut
from app.services.auth_service import AuthService
from app.repositories.user_repo import UserRepository


router = APIRouter(prefix="/auth", tags=["auth"])

auth_service = AuthService(UserRepository())


@router.post("/register", response_model=TokenOut)
async def register(
    payload: RegisterIn,
    session: AsyncSession = Depends(get_db_session),
):
    try:
        token = await auth_service.register(
            session,
            payload.email,
            payload.password,
        )
        return TokenOut(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenOut)
async def login(
    payload: LoginIn,
    session: AsyncSession = Depends(get_db_session),
):
    try:
        token = await auth_service.login(
            session,
            payload.email,
            payload.password,
        )
        return TokenOut(access_token=token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )
