from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_SERVER: str


settings = Settings(_env_file=Path(__file__).parent.parent / ".env",
                    _env_file_encoding="utf-8")
