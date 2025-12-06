from fastapi import HTTPException
from starlette import status



class UserAlreadyExistException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )


class UserNotExistException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )


class UserIncorrectPasswordException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )


class UserNoPermissionException(HTTPException):
     def __init__(self, message: str):
         super().__init__(
             status_code=status.HTTP_403_FORBIDDEN,
             detail=message
         )