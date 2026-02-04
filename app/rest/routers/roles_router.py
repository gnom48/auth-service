from fastapi import APIRouter, Depends, HTTPException
from app.di import di_container
from app.services.role_service import RoleService
from app.models.pydantic import RoleCreate, RolePydantic, User
from ..middleware import verify_jwt

roles_router = APIRouter(prefix="/roles", tags=["Roles"])


@roles_router.post("/", summary="Создание новой роли", response_model=RolePydantic)
async def create_role(
    role: RoleCreate,
    user: User = Depends(verify_jwt),
    service: RoleService = Depends(lambda: di_container.role_service())
):
    return await service.create_role(role)


@roles_router.get("/{role_id}", summary="Получение информации о роли", response_model=RolePydantic)
async def get_role(
    role_id: int,
    user: User = Depends(verify_jwt),
    service: RoleService = Depends(lambda: di_container.role_service())
):
    role = await service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return role


@roles_router.delete("/{role_id}", summary="Удаление роли")
async def delete_role(
    role_id: int,
        user: User = Depends(verify_jwt),
    service: RoleService = Depends(lambda: di_container.role_service())
):
    deleted = await service.delete_role(role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return {"message": "Роль удалена."}
