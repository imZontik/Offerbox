from fastapi.params import Depends

from app.infrastructure.database.dependencies import get_repository_factory
from app.infrastructure.database.factory import RepositoryFactory
from app.modules.auth.repository import UserRepository
from app.modules.auth.services import UserService


async def get_user_service(
        factory: RepositoryFactory = Depends(get_repository_factory)
) -> UserService:
    return UserService(repository=factory.get_repository(UserRepository))