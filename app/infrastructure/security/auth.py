from datetime import datetime

from fastapi.params import Depends
from jose import jwt
from asyncpg.pgproto.pgproto import timedelta
from passlib.context import CryptContext

from app.config.settings import settings
from app.modules.auth.dependencies import get_user_service
from app.modules.auth.models import AuthUserModel
from app.modules.auth.services import UserService

pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],
    deprecated="auto"
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=120)
    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.AUTH_SECRET_KEY,
        settings.AUTH_ALGORITHM
    )

    return encoded_jwt


async def authenticate_user(
        email: str,
        password: str,
        service: UserService = Depends(get_user_service)
) -> AuthUserModel | None:
    user = await service.find_by_email(email)

    if user and verify_password(password, user.hashed_password):
        return user

    return None