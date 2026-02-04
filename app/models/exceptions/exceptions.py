from fastapi import HTTPException
from starlette.status import *


class PermissionDeniedException(HTTPException):
    def __init__(self, detail="Access forbidden", headers=None):
        super().__init__(HTTP_403_FORBIDDEN, detail, headers)


class AuthException(HTTPException):
    def __init__(self, detail="Unauthorized", headers=None):
        super().__init__(HTTP_401_UNAUTHORIZED, detail, headers)


class NotFoundException(HTTPException):
    def __init__(self, detail="Not found resource", headers=None):
        super().__init__(HTTP_404_NOT_FOUND, detail, headers)


class InvalidDataException(HTTPException):
    def __init__(self, detail="Data in model is invalid", headers=None):
        super().__init__(HTTP_400_BAD_REQUEST, detail, headers)
