from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_asyncpg

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
