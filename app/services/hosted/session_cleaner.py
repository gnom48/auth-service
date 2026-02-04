from app.db import SessionRepository
from app.models.sqlalchemy import SessionRecordOrm
from datetime import datetime
import logging


# NOTE: тут ситуация неоднозначная - scheduler вообще плохо работает с asgi, поэтому этот сервис надо запускать либо как отдельный контейнер в 1 эксземпляре,
# либо прикручивать к этому файл/строку блокировки (в бд или celery) для гарантии, что только 1 запустится,
# и то будет хлипко в плане запланировать на конкретное время


class SessionsCleaner:
    def __init__(self, repo: SessionRepository):
        self.repo = repo
        self.logger = logging.getLogger("SessionsCleaner")

    async def cleanup_expired_refresh_tokens(self):
        async with self.repo as r:
            del_count = await r.delete_expired()
            self.logger.debug(
                msg=f"cleanup_expired_refresh_tokens executed delete {del_count} expired sessions at {datetime.now()}")
