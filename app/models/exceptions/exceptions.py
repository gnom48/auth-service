from pydantic import BaseModel


class SqlException:
    msg: str


class PermissionDeniedException(Exception):
    pass


class AuthException(Exception):
    pass
