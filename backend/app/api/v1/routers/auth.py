"""Authentication endpoints — register, login, refresh, me, logout."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token, decode_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    AccessTokenResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    svc = AuthService(db)
    user = await svc.register(data.email, data.password, data.full_name)
    access, refresh = svc.make_tokens(user)
    return TokenResponse(
        access_token=access, refresh_token=refresh, user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    svc = AuthService(db)
    user = await svc.authenticate(data.email, data.password)
    access, refresh = svc.make_tokens(user)
    return TokenResponse(
        access_token=access, refresh_token=refresh, user=UserResponse.model_validate(user)
    )


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)) -> AccessTokenResponse:
    payload = decode_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    user = await UserRepository(db).get_by_id(payload.get("sub", ""))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive"
        )
    return AccessTokenResponse(access_token=create_access_token(str(user.id)))


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(user)


@router.post("/logout")
async def logout(user: User = Depends(get_current_user)) -> dict:
    # Stateless JWT — client apna token delete kare. Server-side revoke baad me.
    return {"success": True, "message": "Logged out"}
