from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.repository import UserRepository


async def get_user_repository(session: AsyncSession) -> UserRepository:
    return UserRepository(session)