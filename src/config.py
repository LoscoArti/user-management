from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_SERVER: str

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings(
    _env_file=Path(__file__).parent.parent / ".env", _env_file_encoding="utf-8"
)
