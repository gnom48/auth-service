from .base_config import BaseConfig


class DbConfig(BaseConfig):
    def __init__(self):
        self.POSTGRES_HOST: str = ""
        self.POSTGRES_PORT: int = 7777
        self.POSTGRES_USER: str = ""
        self.POSTGRES_PASSWORD: str = ""
        self.POSTGRES_DB: str = ""
        self.DROP_TABLES: bool = False
        self.CREATE_TABLES: bool = False

        super().__init__()
