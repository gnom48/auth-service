from app.db.repositories.base_repo import BaseRepository
from app.models.sqlalchemy import UserPermission
from sqlalchemy import select
from typing import List, Optional


class UserPermissionRepository(BaseRepository[UserPermission]):
    model_class = UserPermission

    async def create(self, obj_in: dict) -> Optional[UserPermission]:
        async with self as repo:
            permission = UserPermission(**obj_in)
            self._session.add(permission)
            await self._session.commit()
            await self._session.refresh(permission)
            return permission

    async def read_by_id(self, user_id: str, res_id: int) -> Optional[UserPermission | None]:
        async with self as repo:
            result = await self._session.execute(select(UserPermission)
                                                 .where(UserPermission.user_id == user_id)
                                                 .where(UserPermission.resource_id == res_id))
            return result.scalar_one_or_none()

    async def read_by_user_id(self, user_id: str) -> Optional[List[UserPermission]]:
        async with self as repo:
            result = await self._session.execute(select(UserPermission).where(UserPermission.user_id == user_id))
            return result.scalars().all()

    async def update(self, user_id: str, res_id: int, updated_obj: dict) -> Optional[UserPermission]:
        async with self as repo:
            permission = await self.read_by_id(user_id, res_id)
            if permission:
                for key, value in updated_obj.items():
                    setattr(permission, key, value)
                await self._session.commit()
                await self._session.refresh(permission)
                return permission
            return None

    async def delete(self, user_id: str, res_id: int) -> bool:
        async with self as repo:
            permission = await self.read_by_id(user_id, res_id)
            if permission:
                await self._session.delete(permission)
                await self._session.commit()
                return True
            return False
