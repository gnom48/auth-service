from typing import Optional
from app.db import UserRepository
from app.models.exceptions import AuthException
from app.models.pydantic import UserCreate, UserUpdate, User
from .utils.bcrypt_methods import get_password_hash, verify_password


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.repo = user_repo

    async def create_user(self, user_in: UserCreate) -> Optional[User]:
        hashed_password = get_password_hash(user_in.password)
        user_dict = user_in.dict()
        user_dict["hashed_password"] = hashed_password
        del user_dict['password']
        del user_dict['confirm_password']
        user = await self.repo.create(user_dict)
        return User.model_validate(user)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user = await self.repo.read_by_email(email)
        if not user:
            raise AuthException()
        return User.model_validate(user)

    async def get_user_by_id(self, id: int) -> Optional[User]:
        user = await self.repo.read_by_id(id)
        if not user:
            raise AuthException()
        return User.model_validate(user)

    async def verify_user(self, email: str, plain_password: str) -> Optional[User]:
        """
        Проверяет электронную почту и пароль пользователя.
        Возвращает объект пользователя, если верификация прошла успешно.
        """
        user = await self.repo.read_by_email(email)
        if not user:
            raise AuthException()

        if not verify_password(plain_password, user.hashed_password):
            return None

        return User.model_validate(user)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserUpdate]:
        return await self.repo.update(user_id, user_update.dict())

    async def soft_delete_user(self, user_id: int) -> bool:
        return await self.repo.soft_delete(user_id)
