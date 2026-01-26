from typing import Optional
from app.db import UserRepository
from app.models.exceptions import AuthException
from app.models.pydantic import UserCreate, UserUpdate, User
from .utils.pwd_context import pwd_context


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.repo = user_repo

    async def create_user(self, user_in: UserCreate) -> Optional[UserCreate]:
        hashed_password = pwd_context.hash(user_in.password)
        user_dict = user_in.dict()
        user_dict["hashed_password"] = hashed_password
        del user_dict['password']
        return await self.repo.create(user_dict)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user = await self.repo.read_by_email(email)
        if not user:
            raise AuthException()
        return User.model_validate(user)

    async def verify_user(self, email: str, plain_password: str) -> Optional[User]:
        """
        Проверяет электронную почту и пароль пользователя.
        Возвращает объект пользователя, если верификация прошла успешно.
        """
        user = await self.get_user_by_email(email)
        if not user:
            raise AuthException()

        if not pwd_context.verify(plain_password, user.hashed_password):
            return None

        return user

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserUpdate]:
        return await self.repo.update(user_id, user_update.dict())

    async def delete_user(self, user_id: int) -> bool:
        return await self.repo.delete(user_id)
