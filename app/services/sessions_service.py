from datetime import timedelta, datetime
from typing import Optional
from jose import jwt, exceptions as jwt_exceptions
from app.configs import AuthConfig
from app.db import SessionRepository, UserRepository
from app.models.pydantic import User


class SessionsService:
    def __init__(self, session_repo: SessionRepository, user_repo: UserRepository, config: AuthConfig):
        self.session_repo = session_repo
        self.user_repo = user_repo
        self.config = config

    def generate_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return encoded_jwt

    def generate_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.config.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return encoded_jwt

    async def create_session(self, user_id: int, refresh_token: str):
        session_data = {
            "user_id": user_id,
            "refresh_token": refresh_token,
            "expires_at": datetime.utcnow() + timedelta(days=self.config.REFRESH_TOKEN_EXPIRE_DAYS),
        }
        await self.session_repo.create_session(session_data)

    async def revoke_session(self, refresh_token: str):
        return await self.session_repo.invalidate_session(refresh_token)

    async def refresh_tokens(self, refresh_token: str):
        payload = jwt.decode(refresh_token, self.config.SECRET_KEY, algorithms=[
                             self.config.ALGORITHM])
        if payload is None:
            return None
        user_id = payload.get("sub")
        if user_id is None:
            return None

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

        await self.session_repo.invalidate_session(refresh_token)
        await self.create_session(user_id, new_refresh_token)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    async def validate_token(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[
                                 self.config.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                return None
            return await self.user_repo.read_by_id(user_id)
        except jwt_exceptions.JWTError | jwt_exceptions.JWTClaimsError | jwt_exceptions.ExpiredSignatureError:
            return None
