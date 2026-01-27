from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class PydanticBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(PydanticBase):
    id: str
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: EmailStr


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


class RoleCreate(PydanticBase):
    title: str
    description: Optional[str]


class PermissionCreate(PydanticBase):
    code: str
    name: Optional[str]


class Token(PydanticBase):
    access_token: str
    refresh_token: str
    token_type: str


class OneToken(PydanticBase):
    token: str


class SignInClaims(PydanticBase):
    email: str
    password: str
