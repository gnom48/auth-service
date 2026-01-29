from typing import Optional
from app.db import UserRepository
from app.models.exceptions import AuthException
from app.models.pydantic import UserCreate, UserUpdate, User, RolePydantic, UserPermissionPydantic
from .utils.bcrypt_methods import get_password_hash, verify_password


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.repo = user_repo

    async def create_user(self, user_in: UserCreate) -> Optional[User]:
        async with self.repo as r:
            hashed_password = get_password_hash(user_in.password)
            user_dict = user_in.dict()
            user_dict["hashed_password"] = hashed_password
            del user_dict['password']
            del user_dict['confirm_password']
            user = await r.create(user_dict)
            return User.model_validate_orm(user)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with self.repo as r:
            user = await self.repo.read_by_email(email)
            if not user:
                raise AuthException()
            return User.model_validate_orm(user)

    async def get_user_by_id(self, id: int) -> Optional[User]:
        async with self.repo as r:
            user = await r.read_by_id(id)
            if not user:
                raise AuthException()
            res = User.model_validate_orm(user)
            res.role = RolePydantic.model_validate(user.role)
            res.permissions = [UserPermissionPydantic.model_validate(
                i) for i in user.direct_permissions] or []
            return res

    async def verify_user(self, email: str, plain_password: str) -> Optional[User]:
        """
        Проверяет электронную почту и пароль пользователя.
        Возвращает объект пользователя, если верификация прошла успешно.
        """
        async with self.repo as r:
            user = await r.read_by_email(email)
            if not user:
                raise AuthException()

            if not verify_password(plain_password, user.hashed_password):
                return None

            return User.model_validate_orm(user)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserUpdate]:
        async with self.repo as r:
            if (user := await r.update(user_id, user_update.dict())):
                return User.model_validate_orm(user)
            else:
                return None

    async def soft_delete_user(self, user_id: int) -> bool:
        async with self.repo as r:
            return await r.soft_delete(user_id)
