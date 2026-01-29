from typing import Optional, List
from app.db import UserPermissionRepository, ResourceRepository
from app.models.pydantic import UserPermissionPydantic, ResourceCreate, ResourcePydantic
from app.models.exceptions import NotFoundException


class PermissionService:
    def __init__(self, permission_repo: UserPermissionRepository, resource_repo: ResourceRepository):
        self.permission_repo = permission_repo
        self.resource_repo = resource_repo

    async def create_permission(self, permission_in: UserPermissionPydantic) -> Optional[UserPermissionPydantic]:
        async with self.permission_repo as r:
            if (permission := await r.create(permission_in.dict())):
                return UserPermissionPydantic.model_validate(permission)
            else:
                return None

    async def create_resource(self, resource_in: ResourceCreate) -> Optional[ResourcePydantic]:
        async with self.resource_repo as r:
            if (resource := await r.create(resource_in.dict())):
                return ResourcePydantic.model_validate(resource)
            else:
                return None

    async def delete_resource(self, resource_id: int) -> Optional[bool]:
        async with self.resource_repo as r:
            return await r.delete(resource_id)

    async def update_permission(self, permission_in: UserPermissionPydantic) -> Optional[UserPermissionPydantic]:
        async with self.permission_repo as r:
            if (permission := await r.update(
                    user_id=permission_in.user_id,
                    res_id=permission_in.resource_id,
                    updated_obj=permission_in.dict())):
                return UserPermissionPydantic.model_validate(permission)
            else:
                return None

    async def get_permissions_by_user_id(self, user_id: str) -> List[UserPermissionPydantic]:
        async with self.permission_repo as r:
            return [UserPermissionPydantic.model_validate(i) for i in await r.read_by_user_id(user_id)]

    async def get_permission_by_ids(self, user_id: str, resource_id: int) -> Optional[UserPermissionPydantic]:
        async with self.permission_repo as r:
            if (permission := await r.read_by_id(user_id, resource_id)):
                return UserPermissionPydantic.model_validate(permission)
            else:
                return None

    async def delete_permission(self, user_id: str, permission_id: int) -> bool:
        async with self.permission_repo as r:
            return await r.delete(user_id, permission_id)
