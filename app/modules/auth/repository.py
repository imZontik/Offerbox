from app.infrastructure.database.repository import BaseRepository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.auth.models import AuthUserModel


class UserRepository(BaseRepository[AuthUserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AuthUserModel)

    async def create(self, email: str, hashed_password: str) -> AuthUserModel:
        result = self.model(
            email=email,
            hashed_password=hashed_password
        )
        self.session.add(result)

        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(result)

        return result

    async def find_by_email(self, email: str) -> AuthUserModel | None:
        query = select(AuthUserModel).where(
            AuthUserModel.email == email
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()