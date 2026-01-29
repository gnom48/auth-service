from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from dependency_injector.providers import Factory
from .base_repo import BaseRepository
from app.models.sqlalchemy import UserOrm
from sqlalchemy.orm import joinedload


class UserRepository(BaseRepository[UserOrm]):
    model_class = UserOrm

    async def create(self, obj_in: dict) -> Optional[UserOrm]:
        user = UserOrm(**obj_in)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def read_by_id(self, entity_id: str) -> Optional[UserOrm]:
        result = await self._session.execute(select(UserOrm)
                                             .where(UserOrm.id == entity_id)
                                             .options(joinedload(UserOrm.role), joinedload(UserOrm.direct_permissions)))
        return result.unique().scalar_one_or_none()

    async def read_all(self) -> List[UserOrm]:
        result = await self._session.execute(select(UserOrm).options(joinedload(UserOrm.role), joinedload(UserOrm.direct_permissions)))
        return result.scalars().all()

    async def read_by_email(self, email: str) -> UserOrm:
        result = await self._session.execute(select(UserOrm)
                                             .where(UserOrm.email == email)
                                             .options(joinedload(UserOrm.role), joinedload(UserOrm.direct_permissions)))
        return result.scalars().first()

    async def update(self, entity_id: str, updated_obj: dict) -> Optional[UserOrm]:
        user = await self.read_by_id(entity_id)
        if user:
            for key, value in updated_obj.items():
                setattr(user, key, value)
            await self._session.commit()
            await self._session.refresh(user)
            return user
        return None

    async def delete(self, entity_id: str) -> bool:
        user = await self.read_by_id(entity_id)
        if user:
            await self._session.delete(user)
            await self._session.commit()
            return True
        return False
