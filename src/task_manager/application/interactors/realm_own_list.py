from typing import Protocol, Sequence
from dataclasses import dataclass
from abc import abstractmethod

from task_manager.application.common import (
    AsyncTransactionManager,
)
from task_manager.application.gateways import RealmGateway, UserGateway

from task_manager.domain.models import Realm, UserId


@dataclass
class RealmOwnListDTO:
    user_id: UserId
    pagination_limit: int
    pagination_offset: int


@dataclass
class RealmOwnListResult:
    realms: Sequence[Realm]


class RealmOwnListInteractor(Protocol):
    @abstractmethod
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        task_gateway: RealmGateway,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, data: RealmOwnListDTO) -> RealmOwnListResult:
        raise NotImplementedError


class RealmOwnListInteractorImpl(RealmOwnListInteractor):
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        task_gateway: RealmGateway,
        user_gateway: UserGateway,
    ) -> None:
        self.transaction = transaction
        self.task_gateway = task_gateway
        self.user_gateway = user_gateway

    async def __call__(self, data: RealmOwnListDTO) -> RealmOwnListResult:
        user = await self.user_gateway.get(data.user_id)

        realms = await self.task_gateway.read(
            data.pagination_limit,
            data.pagination_offset,
            owner_uid=user.uid,
        )

        return RealmOwnListResult(realms)
