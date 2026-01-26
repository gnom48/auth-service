from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, BigInteger, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import time


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


user_roles_association = Table(
    'user_roles',
    BaseModelOrm.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    UniqueConstraint('user_id', 'role_id')
)

role_permissions_association = Table(
    'role_permissions',
    BaseModelOrm.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('perm_id', Integer, ForeignKey('permissions.id'), primary_key=True),
    UniqueConstraint('role_id', 'perm_id')
)

user_permissions_association = Table(
    'user_permissions',
    BaseModelOrm.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('perm_id', Integer, ForeignKey('permissions.id'), primary_key=True),
    UniqueConstraint('user_id', 'perm_id')
)


class UserOrm(BaseModelOrm):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    middle_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    roles = relationship(
        "Role", secondary=user_roles_association, back_populates="users")
    direct_permissions = relationship(
        "Permission", secondary=user_permissions_association, back_populates="direct_users")


class RoleOrm(BaseModelOrm):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    permissions = relationship(
        "Permission", secondary=role_permissions_association, back_populates="roles")
    users = relationship(
        "User", secondary=user_roles_association, back_populates="roles")


class PermissionOrm(BaseModelOrm):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))

    roles = relationship(
        "Role", secondary=role_permissions_association, back_populates="permissions")
    direct_users = relationship(
        "User", secondary=user_permissions_association, back_populates="direct_permissions")


class SessionRecordOrm(BaseModelOrm):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    refresh_token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)

    user = relationship("User", backref="sessions")
