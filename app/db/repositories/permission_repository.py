from app.db.repositories.base_repo import BaseRepository
from app.models.sqlalchemy import PermissionOrm
from sqlalchemy import select
from typing import List, Optional


class PermissionRepository(BaseRepository[PermissionOrm]):
    model_class = PermissionOrm

    async def create(self, obj_in: dict) -> Optional[PermissionOrm]:
        async with self as repo:
            permission = PermissionOrm(**obj_in)
            self._session.add(permission)
            await self._session.flush()
            await self._session.refresh(permission)
            return permission

    async def read_by_id(self, entity_id: int) -> Optional[PermissionOrm]:
        async with self as repo:
            result = await self._session.execute(select(PermissionOrm).where(PermissionOrm.id == entity_id))
            return result.scalar_one_or_none()

    async def read_all(self) -> List[PermissionOrm]:
        async with self as repo:
            result = await self._session.execute(select(PermissionOrm))
            return result.scalars().all()

    async def update(self, entity_id: int, updated_obj: dict) -> Optional[PermissionOrm]:
        async with self as repo:
            permission = await self.read_by_id(entity_id)
            if permission:
                for key, value in updated_obj.items():
                    setattr(permission, key, value)
                await self._session.flush()
                await self._session.refresh(permission)
                return permission
            return None

    async def delete(self, entity_id: int) -> bool:
        async with self as repo:
            permission = await self.read_by_id(entity_id)
            if permission:
                await self._session.delete(permission)
                await self._session.flush()
                return True
            return False
