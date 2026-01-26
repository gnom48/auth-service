from typing import Optional
from app.db import RoleRepository
from app.models.pydantic import RoleCreate, RoleUpdate


class RoleService:
    def __init__(self, role_repo: RoleRepository):
        self.repo = role_repo

    async def create_role(self, role_in: RoleCreate) -> Optional[RoleCreate]:
        return await self.repo.create(role_in.dict())

    async def get_role_by_id(self, role_id: int) -> Optional[RoleCreate]:
        return await self.repo.read_by_id(role_id)

    async def update_role(self, role_id: int, role_update: RoleUpdate) -> Optional[RoleUpdate]:
        return await self.repo.update(role_id, role_update.dict())

    async def delete_role(self, role_id: int) -> bool:
        return await self.repo.delete(role_id)
