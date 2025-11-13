from typing import Protocol
from abc import abstractmethod

from task_manager.application.common.transaction import AsyncTransactionManager
from task_manager.domain.models.user import User, UserId


class UserGateway(Protocol):
    @abstractmethod
    def __init__(self, session: AsyncTransactionManager) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, pk: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_existing(self, pk: UserId) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, user: User) -> UserId:
        raise NotImplementedError
