from typing import Optional, List
from app.db import PermissionRepository
from app.models.pydantic import PermissionCreate, PermissionUpdate


class PermissionService:
    def __init__(self, permission_repo: PermissionRepository):
        self.repo = permission_repo

    async def create_permission(self, permission_in: PermissionCreate) -> Optional[PermissionCreate]:
        return await self.repo.create(permission_in.dict())

    async def get_permission_by_id(self, permission_id: int) -> Optional[PermissionCreate]:
        return await self.repo.read_by_id(permission_id)

    async def update_permission(self, permission_id: int, permission_update: PermissionUpdate) -> Optional[PermissionUpdate]:
        return await self.repo.update(permission_id, permission_update.dict())

    async def delete_permission(self, permission_id: int) -> bool:
        return await self.repo.delete(permission_id)
