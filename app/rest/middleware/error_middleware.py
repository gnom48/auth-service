from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging
from app.models.exceptions import *
from sqlalchemy.exc import SQLAlchemyError


async def error_middleware(request: Request, call_next):
    logger = logging.getLogger('error_middleware')
    try:
        resp = await call_next(request)
        return resp
    except SQLAlchemyError as e:
        logger.error("Db error by SQLAlchemy: ", exc_info=True)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"data error": "unable to create/read/update/delete data in DB; data is invalid/not found"}, headers={'content-type': 'application/json'})
    except Exception as e:
        logger.error("Error has been handled: ", exc_info=True)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": e.__str__()}, headers={'content-type': 'application/json'})
