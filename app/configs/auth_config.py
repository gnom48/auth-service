from .base_config import BaseConfig


class AuthConfig(BaseConfig):
    def __init__(self):
        self.SECRET_KEY: str = None
        self.ALGORITHM: str = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
        self.REFRESH_TOKEN_EXPIRE_DAYS: int = 7

        super().__init__()
