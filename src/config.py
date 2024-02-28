from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    AMQP_HOST: str
    AMQP_PORT: int
    AMQP_USER: str
    AMQP_PASS: str
    rabbitmq_routing_key: str
    secret_key: str
    ALGORITHM: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str
    AWS_S3_BUCKET_NAME: str
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def RABBITMQ_URI(self):
        return f"amqp://{self.AMQP_USER}:{self.AMQP_PASS}@{self.AMQP_HOST}:{self.AMQP_PORT}/"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
