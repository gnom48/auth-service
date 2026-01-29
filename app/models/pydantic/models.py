from typing import Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class PydanticBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RoleCreate(PydanticBase):
    title: str
    description: Optional[str]


class RolePydantic(PydanticBase):
    id: int
    title: str
    description: Optional[str]


class ResourceCreate(PydanticBase):
    name: str
    description: Optional[str]


class ResourcePydantic(ResourceCreate):
    id: int


class UserPermissionPydantic(PydanticBase):
    user_id: str
    resource_id: int
    read_permission: bool = False
    read_all_permission: bool = False
    create_permission: bool = False
    update_permission: bool = False
    update_all_permission: bool = False
    delete_permission: bool = False
    delete_all_permission: bool = False


class Token(PydanticBase):
    access_token: str
    refresh_token: str
    token_type: str


class OneToken(PydanticBase):
    token: str


class SignInClaims(PydanticBase):
    email: EmailStr
    password: str


class User(PydanticBase):
    id: str
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: EmailStr
    role: RolePydantic | None
    permissions: List[UserPermissionPydantic]

    @classmethod
    def model_validate_orm(cls, orm_object: object):
        """
        Метод валидирует ORM объект и преобразует его в Pydaintc-модель.

        Проверяется наличие полей 'role' и 'direct_permissions', если поля существуют —
        выполняется дополнительная обработка.
        """
        role = None
        permissions = []

        if hasattr(orm_object, 'role') and orm_object.role is not None:
            role = RolePydantic.model_validate(orm_object.role)

        if hasattr(orm_object, 'direct_permissions'):
            permissions = [
                UserPermissionPydantic.model_validate(p)
                for p in orm_object.direct_permissions
            ]

        return cls(
            id=orm_object.id,
            first_name=orm_object.first_name,
            last_name=orm_object.last_name,
            middle_name=orm_object.middle_name,
            email=orm_object.email,
            role=role,
            permissions=permissions
        )


class UserCreate(PydanticBase):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: EmailStr
    password: str
    confirm_password: str


class UserUpdate(PydanticBase):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    new_password: Optional[str]
    current_password: Optional[str]
