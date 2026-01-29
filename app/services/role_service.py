from typing import Optional
from app.db import RoleRepository
from app.models.pydantic import RoleCreate, RolePydantic


class RoleService:
    def __init__(self, role_repo: RoleRepository):
        self.repo = role_repo

    async def create_role(self, role_in: RoleCreate) -> Optional[RolePydantic]:
        async with self.repo as r:
            if (role := await r.create(role_in.dict())):
                return RolePydantic.model_validate(role)
            else:
                return None

    async def get_role_by_id(self, role_id: int) -> Optional[RolePydantic]:
        async with self.repo as r:
            if (role := await r.read_by_id(role_id)):
                return RolePydantic.model_validate(role)
            else:
                return None

    async def delete_role(self, role_id: int) -> bool:
        async with self.repo as r:
            return await r.delete(role_id)
