from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict


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
    role: RolePydantic
    permissions: List[UserPermissionPydantic]


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
