import asyncio
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator
from fastapi import FastAPI
from app.rest.routers import users_router, roles_router, healthcheck_router, permissions_router, auth_router
from .middleware import jwt_middleware, error_middleware
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
    description="Auth service",
    docs_url="/swagger"
)

asgi_application.middleware("http")(error_middleware)

asgi_application.include_router(users_router)
asgi_application.include_router(permissions_router)
asgi_application.include_router(roles_router)
asgi_application.include_router(healthcheck_router)
asgi_application.include_router(auth_router)
