from typing import Protocol
from dataclasses import dataclass
from abc import abstractmethod

from task_manager.application.common import AsyncTransactionManager
from task_manager.application.gateways.user import UserGateway
from task_manager.application.exceptions import UsernameTakenExeption

from task_manager.domain.services.user import UserService
from task_manager.domain.models.user import UserId


@dataclass
class UserRegisterDTO:
    username: str
    password: str


class UserRegisterInteractor(Protocol):
    @abstractmethod
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        user_gateway: UserGateway,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, data: UserRegisterDTO) -> UserId:
        raise NotImplementedError


class UserRegisterInteractorImpl(UserRegisterInteractor):
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        user_gateway: UserGateway,
    ) -> None:
        self.transaction = transaction
        self.user_gateway = user_gateway

    async def __call__(self, data: UserRegisterDTO) -> UserId:
        if await self.user_gateway.get_by_username(data.username) is not None:
            raise UsernameTakenExeption()

        user = UserService().register(
            username=data.username,
            password=data.password,
        )
        user_id = await self.user_gateway.save(user)

        await self.transaction.commit()

        return user_id
