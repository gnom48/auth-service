from sqlalchemy import BigInteger, Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import time
from app.models.pydantic import User
import uuid


class BaseModelOrm(DeclarativeBase):
    __abstract__ = True
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    who_create: Mapped[str | None] = mapped_column(
        String(36), nullable=True, default=None)
    who_update: Mapped[str | None] = mapped_column(
        String(36), nullable=True, default=None)
    when_create: Mapped[int] = mapped_column(
        BigInteger, default=lambda: int(time.time()))
    when_update: Mapped[int] = mapped_column(BigInteger, default=lambda: int(
        time.time()), onupdate=lambda: int(time.time()))

    def complete_user_fields(self, user: User):
        self.when_create = user.id
        self.when_update = user.id


class UserOrm(BaseModelOrm):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    first_name = Column(String(50))
    last_name = Column(String(50))
    middle_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100))

    roles = relationship("UserRole", back_populates="user")
    direct_permissions = relationship("UserPermission", back_populates="user")


class RoleOrm(BaseModelOrm):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    users = relationship("UserRole", back_populates="role")
    permissions = relationship("RolePermission", back_populates="role")


class PermissionOrm(BaseModelOrm):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))

    roles = relationship("RolePermission", back_populates="permission")
    direct_users = relationship("UserPermission", back_populates="permission")


class UserRole(BaseModelOrm):
    __tablename__ = 'user_roles'

    user_id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)

    user = relationship("UserOrm", back_populates="roles")
    role = relationship("RoleOrm", back_populates="users")

    __table_args__ = (
        UniqueConstraint('user_id', 'role_id'),
    )


class RolePermission(BaseModelOrm):
    __tablename__ = 'role_permissions'

    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    perm_id = Column(Integer, ForeignKey('permissions.id'), primary_key=True)

    role = relationship("RoleOrm", back_populates="permissions")
    permission = relationship("PermissionOrm", back_populates="roles")

    __table_args__ = (
        UniqueConstraint('role_id', 'perm_id'),
    )


class UserPermission(BaseModelOrm):
    __tablename__ = 'user_permissions'

    user_id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    perm_id = Column(Integer, ForeignKey('permissions.id'), primary_key=True)

    user = relationship("UserOrm", back_populates="direct_permissions")
    permission = relationship("PermissionOrm", back_populates="direct_users")

    __table_args__ = (
        UniqueConstraint('user_id', 'perm_id'),
    )


class SessionRecordOrm(BaseModelOrm):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    user_id = Column(String(36), ForeignKey("users.id"))
    refresh_token = Column(String, unique=True, index=True)
    expires_at = Column(Integer)

    user = relationship("UserOrm", backref="sessions")
