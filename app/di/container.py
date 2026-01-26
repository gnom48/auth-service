from dependency_injector.containers import DeclarativeContainer, providers
from dependency_injector import providers
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.db import UserRepository, PermissionRepository, RoleRepository, SessionRepository
from app.db import configure_db
from app.services import UserService, PermissionService, RoleService, SessionsService
from app.configs import *


class Container(DeclarativeContainer):
    configuration = providers.Configuration()

    server_config = providers.Singleton(ServerConfig)
    db_config = providers.Singleton(DbConfig)
    auth_config = providers.Singleton(AuthConfig)

    __db_url = providers.Resource(
        URL.create,
        drivername="postgresql+asyncpg",
        username=db_config.provided.POSTGRES_USER,
        password=db_config.provided.POSTGRES_PASSWORD,
        host=db_config.provided.POSTGRES_HOST,
        port=db_config.provided.POSTGRES_PORT,
        database=db_config.provided.POSTGRES_DB
    )

    __async_engine = providers.Resource(
        create_async_engine,
        url=__db_url,
        echo=False,
        pool_size=5,
        max_overflow=3
    )

    __session_factory = providers.Factory(
        async_sessionmaker[AsyncSession],
        bind=__async_engine,
        expire_on_commit=False
    )

    db_configurer = providers.Callable(
        configure_db,
        async_engine=__async_engine,
        need_create_tables=db_config.provided.CREATE_TABLES,
        need_drop_tables=db_config.provided.DROP_TABLES
    )

    user_repository = providers.Factory(
        UserRepository, session_factory=__session_factory)
    role_repository = providers.Factory(
        RoleRepository, session_factory=__session_factory)
    permission_repository = providers.Factory(
        PermissionRepository, session_factory=__session_factory)
    session_repository = providers.Factory(
        SessionRepository, session_factory=__session_factory)

    user_service = providers.Factory(UserService, user_repo=user_repository)
    role_service = providers.Factory(RoleService, role_repo=role_repository)
    permission_service = providers.Factory(
        PermissionService, permission_repo=permission_repository)
    session_service = providers.Factory(
        SessionsService, session_repo=session_repository, user_repo=user_repository, config=auth_config)
