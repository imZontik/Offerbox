from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing_extensions import AsyncGenerator

from app.config.settings import settings

engine = create_async_engine(str(settings.LOCAL_DATABASE_URL or settings.DATABASE_URL))
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass