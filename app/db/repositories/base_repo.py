import logging
from abc import ABCMeta
from typing import Generic, TypeVar, Any, Optional
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
import logging
from app.models.sqlalchemy import BaseModelOrm
from app.models.pydantic import User


T = TypeVar('T', bound=BaseModelOrm)


class BaseRepository(Generic[T], metaclass=ABCMeta):
    """
    Дженерик класс репозитория.

    Для использования передать в конструктор сессию БД (эксперимент, чтобы управлять подключениями к БД извне т.е. из сервисов)
    """
    model_class: Any

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.__session_factory = session_factory
        self._session: AsyncSession = None
        self._logger = logging.getLogger(name="repo")

    # async with

    async def dispose(self):
        await self._session.close()

    async def __aenter__(self):
        self._session = self.__session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.dispose()

    # virtual methods

    async def create(self, obj_in: dict) -> Optional[T]:
        logging.error(
            f"Method create not implementer for model <{self.model_class.__name__}>")
        return None

    async def read_by_id(self, entity_id: int | str) -> Optional[T]:
        logging.error(
            f"Method read_by_id not implementer for model <{self.model_class.__name__}>")
        return None

    async def read_all(self) -> Optional[T]:
        logging.error(
            f"Method read_all not implementer for model <{self.model_class.__name__}>")
        return None

    async def update(self, entity_id: int | str, updated_obj: dict) -> Optional[T]:
        logging.error(
            f"Method update not implementer for model <{self.model_class.__name__}>")
        return None

    async def delete(self, entity_id: int | str) -> bool:
        logging.error(
            f"Method delete not implementer for model <{self.model_class.__name__}>")
        return False

    async def soft_delete(self, entity_id: int | str) -> bool:
        async with self as repo:
            entity = await self.read_by_id(entity_id)
            if entity:
                await self._session.execute(update(self.model_class).where(self.model_class.id == entity_id).values(is_deleted=True))
                await self._session.commit()
                return True
            return False
