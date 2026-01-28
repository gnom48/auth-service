from fastapi import APIRouter, Depends, HTTPException
from app.di import di_container
from app.services.permission_service import PermissionService
from app.models.pydantic import UserPermissionPydantic, User, ResourceCreate, ResourcePydantic
from ..middleware import verify_jwt
from starlette.status import HTTP_404_NOT_FOUND


permissions_router = APIRouter(prefix="/permissions", tags=["Permissions"])
resources_router = APIRouter(prefix="/resources", tags=["Resources"])


@resources_router.post("/", summary="Создание нового ресурса", response_model=ResourcePydantic)
async def create_resource(
    resource: ResourceCreate,
        user: User = Depends(verify_jwt),
    service: PermissionService = Depends(
        lambda: di_container.permission_service())
):
    return await service.create_resource(resource)


@resources_router.delete("/", summary="Удаление ресурса", response_model=ResourcePydantic)
async def delete_resource(
    resource_id: int,
    user: User = Depends(verify_jwt),
    service: PermissionService = Depends(
        lambda: di_container.permission_service())
):
    deleted = await service.delete_resource(resource_id)
    if not deleted:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Ресурс не найден.")
    return {"message": "Ресурс и связанные с ним разрешения удалены."}


@permissions_router.post("/", summary="Создание нового разрешения")
async def create_permission(
    permission: UserPermissionPydantic,
    user: User = Depends(verify_jwt),
    service: PermissionService = Depends(
        lambda: di_container.permission_service())
):
    return await service.create_permission(permission)


@permissions_router.get("/{permission_id}/user/{target_user_id}", summary="Получение информации о разрешении")
async def get_permission(
    permission_id: int,
    target_user_id: str,
    user: User = Depends(verify_jwt),
    service: PermissionService = Depends(
        lambda: di_container.permission_service())
):
    permission = await service.get_permission_by_id(permission_id)
    if not permission:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Разрешение не найдено")
    return permission


@permissions_router.put("/", summary="Обновление информации в разрешении")
async def update_permission(
    permission_upd: UserPermissionPydantic,
    user: User = Depends(verify_jwt),
    service: PermissionService = Depends(
        lambda: di_container.permission_service())
):
    permission = await service.update_permission(permission_upd)
    if not permission:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Разрешение не найдено")
    return permission


@permissions_router.delete("/{permission_id}", summary="Удаление разрешения")
async def delete_permission(
    target_user_id: str,
    permission_id: int,
    user: User = Depends(verify_jwt),
    service: PermissionService = Depends(
        lambda: di_container.permission_service())
):
    deleted = await service.delete_permission(target_user_id, permission_id)
    if not deleted:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Разрешение не найдено")
    return {"message": "Разрешение удалено."}
