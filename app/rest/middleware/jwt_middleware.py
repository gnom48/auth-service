from fastapi import HTTPException, Depends
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from typing import Annotated, Optional
from app.services import SessionsService
from app.di import di_container


TOKEN_SCHEME = HTTPBearer(auto_error=False)

EXCLUDED_PATHS = [
    "/auth",
    "/users/sign_up",
    "/health_check",
    "/swagger",
    "/openapi.json"
]


async def verify_jwt(
        credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(
            TOKEN_SCHEME)]
):
    """Проверка JWT токена и объявление о необходимости HTTP-заголовка Authorization."""

    if not credentials:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="No token")

    try:
        token = credentials.credentials

        sessions_service: SessionsService = di_container.session_service()

        user = await sessions_service.validate_token(token)
        if not user:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                                detail="Invalid token")
        return user
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=str(e))
