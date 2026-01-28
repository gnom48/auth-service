import asyncio
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator
from fastapi import FastAPI
from app.rest.routers import users_router, roles_router, healthcheck_router, permissions_router, resources_router, auth_router
from .middleware import error_middleware
from app.di import di_container


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None, None]:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug("Logger configured")

    await di_container.db_configurer()
    logging.debug("Db postgres connected")

    try:
        yield
    except Exception as e:
        logging.error("Error in hosted service: ", exc_info=e)
    finally:
        logging.debug("Hosted services stopped")
        logging.debug("Server stopped")


asgi_application = FastAPI(
    lifespan=lifespan,
    title="Auth Service API",
    version="1.0.0",
    description="""
## Описание сервиса аутентификации

Данный сервис предоставляет функциональность для авторизации и аутентификации пользователей. Он построен на основе JSON Web Tokens (JWT) и предоставляет надёжные инструменты для безопасного доступа к ресурсам приложений.

### Ключевые возможности:
- Аутентификация пользователей через JWT.
- Поддержка ролей и разрешений (RBAC).
- Генерация и обновление токенов.
- Эффективное управление сессиями.

### Концепция работы:
- Пользователи регистрируются и входят в систему, получая токены.
- Каждый запрос сопровождается access-токеном, который проверяется сервером.
- Для продления срока действия токенов предусмотрен refresh-токен.
- Средства защиты включают ограничение числа попыток входа и отслеживание сессий.
""",
    contact={
        "name": "Support Team",
        "url": "https://gnom48.ru",
        "email": "main@gnom48.ru"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Методы для авторизации и аутентификации."
        },
        {
            "name": "Users",
            "description": "Методы для управления пользователями."
        },
        {
            "name": "Roles",
            "description": "Методы для управления ролями."
        },
        {
            "name": "Permissions",
            "description": "Методы для управления разрешениями."
        },
        {
            "name": "Healthcheck",
            "description": "Служебные методы."
        },
        {
            "name": "Resources",
            "description": "Методы управления ресурсами, на которые распространяются разрешения."
        },
    ],
    servers=[
        {
            "url": f"http://localhost:{di_container.server_config().SERVER_PORT}",
            "description": "Your local development server"
        },
        {
            "url": "https://auth.gnom48.ru",
            "description": "Production server"
        }
    ],
    docs_url="/swagger"
)

asgi_application.middleware("http")(error_middleware)

asgi_application.include_router(users_router)
asgi_application.include_router(permissions_router)
asgi_application.include_router(roles_router)
asgi_application.include_router(healthcheck_router)
asgi_application.include_router(auth_router)
asgi_application.include_router(resources_router)
