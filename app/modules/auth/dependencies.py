from uuid import UUID

from fastapi.params import Depends

from fastapi import HTTPException
from fastapi.params import Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError
from starlette import status

from app.config.settings import settings
from app.infrastructure.database.dependencies import get_repository_factory
from app.infrastructure.database.factory import RepositoryFactory
from app.modules.auth.models import UserModel
from app.modules.auth.repository import UserRepository
from app.modules.auth.services import UserService

bearer_scheme = HTTPBearer(auto_error=True)


async def get_user_service(
        factory: RepositoryFactory = Depends(get_repository_factory)
) -> UserService:
    return UserService(repository=factory.get_repository(UserRepository))


async def get_user(
        creds: HTTPAuthorizationCredentials = Security(bearer_scheme),
        service: UserService = Depends(get_user_service),
) -> UserModel:
    try:
        payload = jwt.decode(
            creds.credentials,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM],
            options={"verify_aud": False},
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = UUID(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    user = await service.find_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user