from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from app.models.pydantic import SignInClaims, Token
from app.di import di_container
from app.services import SessionsService, UserService
from app.configs import AuthConfig


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/sign_in", response_model=Token)
async def login_and_get_tokens(
    claims: SignInClaims,
    sessions_service: SessionsService = Depends(
        lambda: di_container.session_service()),
    user_service: UserService = Depends(lambda: di_container.user_service()),
    config: AuthConfig = Depends(lambda: di_container.auth_config())
):
    user = await user_service.verify_user(email=claims.email, plain_password=claims.password)

    access_token_expires = timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = sessions_service.generate_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    refresh_token = sessions_service.generate_refresh_token(
        data={"sub": user.id},
        expires_delta=refresh_token_expires
    )

    await sessions_service.create_session(user.id, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@auth_router.post("/refresh", response_model=Token)
async def refresh_tokens(
    refresh_token: Annotated[str, Body(description="Refresh token")],
    service: SessionsService = Depends(lambda: di_container.session_service())
):
    refresh_token = refresh_token.refresh_token
    tokens = await service.refresh_tokens(refresh_token)
    if tokens is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return tokens


@auth_router.post("/sign_out")
async def logout(
    refresh_token: Annotated[str, Body(description="Refresh token")],
    service: SessionsService = Depends(lambda: di_container.session_service())
):
    refresh_token = refresh_token.refresh_token
    success = await service.revoke_session(refresh_token)
    if not success:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return {"detail": "Logged out successfully"}
