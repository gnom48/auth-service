from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: EmailStr
    password: str
    confirm_password: str


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    new_password: Optional[str]
    current_password: Optional[str]


class RoleCreate(BaseModel):
    title: str
    description: Optional[str]


class RoleUpdate(RoleCreate):
    pass


class PermissionCreate(BaseModel):
    code: str
    name: Optional[str]


class PermissionUpdate(PermissionCreate):
    pass


class TokenData(BaseModel):
    email: Optional[str] = None
    scopes: List[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class SignInClaims(BaseModel):
    email: str
    password: str
