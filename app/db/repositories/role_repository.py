from app.db.repositories.base_repo import BaseRepository
from app.models.sqlalchemy import RoleOrm
from sqlalchemy import select
from typing import List, Optional


class RoleRepository(BaseRepository[RoleOrm]):
    model_class = RoleOrm

    async def create(self, obj_in: dict) -> Optional[RoleOrm]:
        async with self as repo:
            role = RoleOrm(**obj_in)
            self._session.add(role)
            await self._session.flush()
            await self._session.refresh(role)
            return role

    async def read_by_id(self, entity_id: int) -> Optional[RoleOrm]:
        async with self as repo:
            result = await self._session.execute(select(RoleOrm).where(RoleOrm.id == entity_id))
            return result.scalar_one_or_none()

    async def read_all(self) -> List[RoleOrm]:
        async with self as repo:
            result = await self._session.execute(select(RoleOrm))
            return result.scalars().all()

    async def update(self, entity_id: int, updated_obj: dict) -> Optional[RoleOrm]:
        async with self as repo:
            role = await self.read_by_id(entity_id)
            if role:
                for key, value in updated_obj.items():
                    setattr(role, key, value)
                await self._session.flush()
                await self._session.refresh(role)
                return role
            return None

    async def delete(self, entity_id: int) -> bool:
        async with self as repo:
            role = await self.read_by_id(entity_id)
            if role:
                await self._session.delete(role)
                await self._session.flush()
                return True
            return False
