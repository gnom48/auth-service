from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, delete
from .base_repo import BaseRepository
from app.models.sqlalchemy import SessionRecordOrm


class SessionRepository(BaseRepository[SessionRecordOrm]):
    model_class = SessionRecordOrm

    async def create_session(self, obj_in: dict) -> Optional[SessionRecordOrm]:
        session_record = SessionRecordOrm(**obj_in)
        self._session.add(session_record)
        await self._session.commit()
        await self._session.refresh(session_record)
        return session_record

    async def get_session_by_refresh_token(self, refresh_token: str) -> Optional[SessionRecordOrm]:
        result = await self._session.execute(
            select(SessionRecordOrm).where(SessionRecordOrm.refresh_token == refresh_token))
        return result.scalar_one_or_none()

    async def invalidate_session(self, refresh_token: str) -> bool:
        session_record = await self.get_session_by_refresh_token(refresh_token)
        if session_record:
            await self._session.delete(session_record)
            await self._session.commit()
            return True
        return False

    async def get_sessions_by_user_id(self, user_id: int) -> List[SessionRecordOrm]:
        result = await self._session.execute(
            select(SessionRecordOrm).where(SessionRecordOrm.user_id == user_id))
        return result.scalars().all()

    async def delete_expired(self) -> int:
        result = await self._session.execute(
            delete(SessionRecordOrm).where(SessionRecordOrm.expires_at <= datetime.utcnow()).returning(SessionRecordOrm.id))
        return len(result.fetchall())
