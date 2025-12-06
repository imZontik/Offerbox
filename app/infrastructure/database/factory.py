from typing import TypeVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class RepositoryFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_repository(self, repository_class: Type[T]):
        return repository_class(self.session)