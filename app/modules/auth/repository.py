from app.infrastructure.database.repository import BaseRepository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.auth.models import UserModel


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    async def create(self, email: str, hashed_password: str) -> UserModel:
        result = self.model(
            email=email,
            hashed_password=hashed_password
        )
        self.session.add(result)

        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(result)

        return result

    async def find_by_email(self, email: str) -> UserModel | None:
        query = select(UserModel).where(
            UserModel.email == email
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()