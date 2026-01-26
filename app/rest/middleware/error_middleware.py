from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
import logging
from app.models.exceptions import *


async def error_middleware(request: Request, call_next):
    try:
        resp = await call_next(request)
        return resp
    except HTTPException as e:
        raise
    except Exception as e:
        l = logging.getLogger('error_middleware')
        l.error("Error has been handled: ", exc_info=True)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": e.__str__()}, headers={'content-type': 'application/json'})
