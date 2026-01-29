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
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("RoleOrm", back_populates="users", lazy="selectin")
    direct_permissions = relationship(
        "UserPermissionOrm", back_populates="user", lazy="selectin")


class RoleOrm(BaseModelOrm):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    users = relationship("UserOrm", back_populates="role", lazy="selectin")


class ResourceOrm(BaseModelOrm):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    permissions = relationship("UserPermissionOrm", back_populates="resource")


class UserPermissionOrm(BaseModelOrm):
    __tablename__ = 'user_permissions'

    user_id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.id'), primary_key=True)

    read_permission = Column(Boolean, default=False)
    read_all_permission = Column(Boolean, default=False)
    create_permission = Column(Boolean, default=False)
    update_permission = Column(Boolean, default=False)
    update_all_permission = Column(Boolean, default=False)
    delete_permission = Column(Boolean, default=False)
    delete_all_permission = Column(Boolean, default=False)

    user = relationship(
        "UserOrm", back_populates="direct_permissions", lazy="selectin")
    resource = relationship(
        "ResourceOrm", back_populates="permissions", lazy="selectin")

    __table_args__ = (UniqueConstraint('user_id', 'resource_id'),)


class SessionRecordOrm(BaseModelOrm):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    user_id = Column(String(36), ForeignKey("users.id"))
    refresh_token = Column(String, unique=True, index=True)
    expires_at = Column(Integer)

    user = relationship("UserOrm", backref="sessions", lazy="selectin")
