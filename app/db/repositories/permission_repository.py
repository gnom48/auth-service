from app.db.repositories.base_repo import BaseRepository
from app.models.sqlalchemy import UserPermissionOrm
from sqlalchemy import select
from typing import List, Optional


class UserPermissionRepository(BaseRepository[UserPermissionOrm]):
    model_class = UserPermissionOrm

    async def create(self, obj_in: dict) -> Optional[UserPermissionOrm]:
        permission = UserPermissionOrm(**obj_in)
        self._session.add(permission)
        await self._session.commit()
        await self._session.refresh(permission)
        return permission

    async def read_by_id(self, user_id: str, res_id: int) -> Optional[UserPermissionOrm | None]:
        result = await self._session.execute(select(UserPermissionOrm)
                                             .where(UserPermissionOrm.user_id == user_id)
                                             .where(UserPermissionOrm.resource_id == res_id))
        return result.scalar_one_or_none()

    async def read_by_user_id(self, user_id: str) -> Optional[List[UserPermissionOrm]]:
        result = await self._session.execute(select(UserPermissionOrm).where(UserPermissionOrm.user_id == user_id))
        return result.scalars().all()

    async def update(self, user_id: str, res_id: int, updated_obj: dict) -> Optional[UserPermissionOrm]:
        permission = await self.read_by_id(user_id, res_id)
        if permission:
            for key, value in updated_obj.items():
                setattr(permission, key, value)
            await self._session.commit()
            await self._session.refresh(permission)
            return permission
        return None

    async def delete(self, user_id: str, res_id: int) -> bool:
        permission = await self.read_by_id(user_id, res_id)
        if permission:
            await self._session.delete(permission)
            await self._session.commit()
            return True
        return False
