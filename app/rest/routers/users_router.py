from fastapi import APIRouter, Depends, HTTPException
from app.di import di_container
from app.services.user_service import UserService
from app.models.pydantic import UserCreate, UserUpdate, User
from ..middleware import verify_jwt


users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/sign_up", summary="Регистрация пользователя")
async def register_user(
    user: UserCreate,
    service: UserService = Depends(lambda: di_container.user_service())
):
    return await service.create_user(user)


@users_router.get("/{user_id}", summary="Получение информации о пользователе")
async def get_user(
    target_user_id: str,
    user: User = Depends(verify_jwt),
    service: UserService = Depends(lambda: di_container.user_service())
):
    target_user = await service.get_user_by_id(target_user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return target_user


@users_router.put("/{user_id}", summary="Обновление информации о пользователе")
async def update_user(
    target_user_id: str,
    user_update: UserUpdate,
    user: User = Depends(verify_jwt),
    service: UserService = Depends(lambda: di_container.user_service())
):
    updated_user = await service.update_user(target_user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return updated_user


@users_router.delete("/{user_id}", summary="Удаление пользователя (логическое)")
async def delete_user(
    target_user_id: str,
    user: User = Depends(verify_jwt),
    service: UserService = Depends(lambda: di_container.user_service())
):
    deleted = await service.soft_delete_user(target_user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "Пользователь удален."}
