from datetime import timedelta
from typing import Optional
from jose import jwt, exceptions as jwt_exceptions
from app.configs import AuthConfig
from app.db import SessionRepository, UserRepository
from app.models.pydantic import User
import time


class SessionsService:
    def __init__(self, session_repo: SessionRepository, user_repo: UserRepository, config: AuthConfig):
        self.session_repo = session_repo
        self.user_repo = user_repo
        self.config = config

    def generate_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        now = int(time.time())
        if expires_delta:
            expire = now + int(expires_delta.total_seconds())
        else:
            expire = now + self.config.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return encoded_jwt

    def generate_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        now = int(time.time())
        if expires_delta:
            expire = now + int(expires_delta.total_seconds())
        else:
            expire = now + self.config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return encoded_jwt

    async def create_session(self, user_id: int, refresh_token: str):
        async with self.session_repo as r:
            session_data = {
                "user_id": user_id,
                "refresh_token": refresh_token,
                "expires_at": int(time.time()) + self.config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            }
            await r.create_session(session_data)

    async def revoke_session(self, refresh_token: str):
        async with self.session_repo as r:
            return await r.invalidate_session(refresh_token)

    async def refresh_tokens(self, refresh_token: str):
        payload = jwt.decode(refresh_token, self.config.SECRET_KEY, algorithms=[
                             self.config.ALGORITHM])
        if payload is None:
            return None
        user_id = payload.get("sub")
        if user_id is None:
            return None

        async with self.session_repo as r:
            session_record = await self.session_repo.get_session_by_refresh_token(refresh_token)
            if session_record is None:
                return None

            access_token_expires = timedelta(
                minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES)
            new_access_token = self.generate_access_token(
                data={"sub": user_id},
                expires_delta=access_token_expires
            )

            new_refresh_token = self.generate_refresh_token(
                data={"sub": user_id}
            )

            await r.invalidate_session(refresh_token)
            await self.create_session(user_id, new_refresh_token)

            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }

    async def validate_token(self, token: str) -> Optional[User]:
        async with self.user_repo as r:
            try:
                payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[
                    self.config.ALGORITHM])
                user_id = payload.get("sub")
                if user_id is None:
                    return None
                return User.model_validate_orm(await r.read_by_id(user_id))
            except (jwt_exceptions.JWTError, jwt_exceptions.JWTClaimsError, jwt_exceptions.ExpiredSignatureError) as e:
                return None
