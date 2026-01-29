from app.db.repositories.base_repo import BaseRepository
from app.models.sqlalchemy import ResourceOrm
from sqlalchemy import select
from typing import List, Optional


class ResourceRepository(BaseRepository[ResourceOrm]):
    model_class = ResourceOrm

    async def create(self, obj_in: dict) -> Optional[ResourceOrm]:
        resource = ResourceOrm(**obj_in)
        self._session.add(resource)
        await self._session.commit()
        await self._session.refresh(resource)
        return resource

    async def read_by_id(self, entity_id: int) -> Optional[ResourceOrm]:
        result = await self._session.execute(select(ResourceOrm).where(ResourceOrm.id == entity_id))
        return result.scalar_one_or_none()

    async def read_all(self) -> List[ResourceOrm]:
        result = await self._session.execute(select(ResourceOrm))
        return result.scalars().all()

    async def update(self, entity_id: int, updated_obj: dict) -> Optional[ResourceOrm]:
        resource = await self.read_by_id(entity_id)
        if resource:
            for key, value in updated_obj.items():
                setattr(resource, key, value)
            await self._session.commit()
            await self._session.refresh(resource)
            return resource
        return None

    async def delete(self, entity_id: int) -> bool:
        resource = await self.read_by_id(entity_id)
        if resource:
            await self._session.delete(resource)
            await self._session.commit()
            return True
        return False
