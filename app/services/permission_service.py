from typing import Optional, List
from app.db import UserPermissionRepository, ResourceRepository
from app.models.pydantic import UserPermissionPydantic, ResourceCreate, ResourcePydantic


class PermissionService:
    def __init__(self, permission_repo: UserPermissionRepository, resource_repo: ResourceRepository):
        self.permission_repo = permission_repo
        self.resource_repo = resource_repo

    async def create_permission(self, permission_in: UserPermissionPydantic) -> Optional[UserPermissionPydantic]:
        return UserPermissionPydantic.model_validate(await self.permission_repo.create(permission_in.dict()))

    async def create_resource(self, resource_in: ResourceCreate) -> Optional[ResourcePydantic]:
        return ResourcePydantic.model_validate(await self.resource_repo.create(resource_in.dict()))

    async def delete_resource(self, resource_id: int) -> Optional[bool]:
        return await self.resource_repo.delete(resource_id)

    async def update_permission(self, permission_in: UserPermissionPydantic) -> Optional[UserPermissionPydantic]:
        return UserPermissionPydantic.model_validate(await self.permission_repo.create(permission_in.dict()))

    async def get_permissions_by_user_id(self, user_id: str) -> Optional[List[UserPermissionPydantic]]:
        return [UserPermissionPydantic.model_validate(i) for i in await self.permission_repo.read_by_user_id(user_id)]

    async def delete_permission(self, user_id: str, permission_id: int) -> bool:
        return await self.permission_repo.delete(user_id, permission_id)
