from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from app.common.exceptions.users import UserAlreadyExistException, UserNotExistException, UserIncorrectPasswordException
from app.infrastructure.security.auth import get_password_hash, verify_password, create_access_token
from app.modules.auth.dependencies import get_user_service
from app.modules.auth.schemas import UserResponse, AuthRequest, TokenResponse
from app.modules.auth.services import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"]
)


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def register(
        data: AuthRequest,
        service: UserService = Depends(get_user_service)
):
    user = await service.find_by_email(email=str(data.email))

    if user:
        raise UserAlreadyExistException(f"Пользователь с email='{data.email}' уже существует")

    hashed_password = get_password_hash(data.password)
    user = await service.create_user(
        email=str(data.email),
        hashed_password=hashed_password,
    )

    return user


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse
)
async def login(
        data: AuthRequest,
        service: UserService = Depends(get_user_service)
):
    user = await service.find_by_email(email=str(data.email))

    if not user:
        raise UserNotExistException(f"Пользователь с email='{data.email}' не существует")

    if not verify_password(data.password, user.hashed_password):
        raise UserIncorrectPasswordException("Пароль не подходит")

    access_token = create_access_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        token_type="Bearer"
    )