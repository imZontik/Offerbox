from typing import TypeVar, Generic, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    def __init__(
            self,
            session: AsyncSession,
            model: type[ModelT]
    ):
        self.session = session
        self.model = model

    async def find_by_id_or_none(self, model_id: UUID) -> ModelT | None:
        query = select(self.model).where(
            self.model.id == model_id
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def find_all(self) -> List[ModelT]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())