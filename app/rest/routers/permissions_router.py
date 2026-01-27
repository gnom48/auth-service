from fastapi import APIRouter, Depends, HTTPException
from app.di import di_container
from app.services.permission_service import PermissionService
from app.models.pydantic import PermissionCreate, User
from ..middleware import verify_jwt


permissions_router = APIRouter(prefix="/permissions", tags=["Permissions"])


@permissions_router.post("/", summary="Создание нового разрешения")
async def create_permission(
    permission: PermissionCreate,
        user: User = Depends(verify_jwt),
    service: PermissionService = Depends(
        lambda: di_container.permission_service())
):
    return await service.create_permission(permission)


@permissions_router.get("/{permission_id}", summary="Получение информации о разрешении")
async def get_permission(
    permission_id: int,
        user: User = Depends(verify_jwt),
    service: PermissionService = Depends(
        lambda: di_container.permission_service())
):
    permission = await service.get_permission_by_id(permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Разрешение не найдено")
    return permission


@permissions_router.delete("/{permission_id}", summary="Удаление разрешения")
async def delete_permission(
    permission_id: int,
        user: User = Depends(verify_jwt),
    service: PermissionService = Depends(
        lambda: di_container.permission_service())
):
    deleted = await service.delete_permission(permission_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Разрешение не найдено")
    return {"message": "Разрешение удалено."}
