from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.base import get_session
from app.infrastructure.database.factory import RepositoryFactory


async def get_repository_factory(
        session: AsyncSession = Depends(get_session)
) -> RepositoryFactory:
    return RepositoryFactory(session)