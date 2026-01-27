from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


class PermissionDeniedException(HTTPException):
    def __init__(self, detail="Access forbidden", headers=None):
        super().__init__(HTTP_403_FORBIDDEN, detail, headers)


class AuthException(HTTPException):
    def __init__(self, detail="Unauthorized", headers=None):
        super().__init__(HTTP_401_UNAUTHORIZED, detail, headers)
