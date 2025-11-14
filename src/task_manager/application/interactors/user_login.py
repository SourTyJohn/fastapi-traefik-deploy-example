from typing import Protocol
from abc import abstractmethod

from task_manager.application.common import AsyncTransactionManager
from task_manager.application.common.encryption import EncryptionContext
from task_manager.application.gateways.user import UserGateway
from task_manager.application.exceptions import InvalidCredentialsException
from task_manager.domain.models.user import UserId


class UserLoginInteractor(Protocol):
    @abstractmethod
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        user_gateway: UserGateway,
        encryption_context: EncryptionContext,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, username: str, password: str) -> UserId:
        raise NotImplementedError


class UserLoginInteractorImpl(UserLoginInteractor):
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        user_gateway: UserGateway,
        encryption_context: EncryptionContext,
    ) -> None:
        self.transaction = transaction
        self.user_gateway = user_gateway
        self.encryption_context = encryption_context

    async def __call__(self, username: str, password: str) -> UserId:
        user = await self.user_gateway.read_by_username(username)
        if user is None:
            raise InvalidCredentialsException()

        hashed_password = user.password

        if not self.encryption_context.verify(password, hashed_password):
            raise InvalidCredentialsException()

        if user.uid is None:
            raise InvalidCredentialsException()

        return user.uid
