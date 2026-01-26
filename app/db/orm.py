from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

from app.models.sqlalchemy.models import *


async def configure_db(
    async_engine: AsyncEngine,
    need_create_tables: bool = False,
    need_drop_tables: bool = False
):
    async with async_engine.begin() as conn:
        check = await conn.execute(text("SELECT 1"))
        if (list(check)[0][0] != 1):
            raise Exception("Database is unavailable")

        if (need_drop_tables):
            await conn.run_sync(BaseModelOrm.metadata.drop_all)

        if (need_create_tables):
            await conn.run_sync(BaseModelOrm.metadata.create_all)
