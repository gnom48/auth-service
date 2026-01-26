from datetime import datetime
from fastapi import APIRouter, status

healthcheck_router = APIRouter(prefix="",
                               tags=["Healthcheck"])


@healthcheck_router.get("/health_check", status_code=status.HTTP_200_OK, description="Health check inside service")
async def server_config_get():
    return {"datetime": datetime.now()}
