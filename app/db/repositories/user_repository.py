from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from dependency_injector.providers import Factory
from .base_repo import BaseRepository
from app.models.sqlalchemy import UserOrm


class UserRepository(BaseRepository[UserOrm]):
    model_class = UserOrm

    async def create(self, obj_in: dict) -> Optional[UserOrm]:
        async with self as repo:
            user = UserOrm(**obj_in)
            self._session.add(user)
            await self._session.commit()
            await self._session.refresh(user)
            return user

    async def read_by_id(self, entity_id: str) -> Optional[UserOrm]:
        async with self as repo:
            result = await self._session.execute(select(UserOrm).where(UserOrm.id == entity_id))
            return result.scalar_one_or_none()

    async def read_all(self) -> List[UserOrm]:
        async with self as repo:
            result = await self._session.execute(select(UserOrm))
            return result.scalars().all()

    async def read_by_email(self, email: str) -> UserOrm:
        async with self as repo:
            result = await self._session.execute(select(UserOrm).where(UserOrm.email == email))
            return result.scalars().first()

    async def update(self, entity_id: str, updated_obj: dict) -> Optional[UserOrm]:
        async with self as repo:
            user = await self.read_by_id(entity_id)
            if user:
                for key, value in updated_obj.items():
                    setattr(user, key, value)
                await self._session.commit()
                await self._session.refresh(user)
                return user
            return None

    async def delete(self, entity_id: str) -> bool:
        async with self as repo:
            user = await self.read_by_id(entity_id)
            if user:
                await self._session.delete(user)
                await self._session.commit()
                return True
            return False
