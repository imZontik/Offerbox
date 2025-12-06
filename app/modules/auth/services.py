from app.modules.auth.models import AuthUserModel
from app.modules.auth.repository import UserRepository
from uuid import UUID


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, email: str, hashed_password: str) -> AuthUserModel:
        return await self.repository.create(
            email=email,
            hashed_password=hashed_password
        )

    async def find_by_id(self, user_id: UUID) -> AuthUserModel | None:
        return await self.repository.find_by_id_or_none(model_id=user_id)

    async def find_by_email(self, email: str) -> AuthUserModel | None:
        return await self.repository.find_by_email(email=email)