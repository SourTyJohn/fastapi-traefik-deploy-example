from typing import Protocol
from dataclasses import dataclass
from abc import abstractmethod

from task_manager.application.common import (
    AsyncTransactionManager,
)
from task_manager.application.gateways import RealmGateway, UserGateway

from task_manager.domain.services.realm import RealmService
from task_manager.domain.models import RealmId, UserId


@dataclass
class RealmCreateDTO:
    user_id: UserId
    task_name: str
    task_description: str


@dataclass
class RealmCreateResult:
    realm_id: RealmId


class RealmCreateInteractor(Protocol):
    @abstractmethod
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        task_gateway: RealmGateway,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, data: RealmCreateDTO) -> RealmCreateResult:
        raise NotImplementedError


class RealmCreateInteractorImpl(RealmCreateInteractor):
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        task_gateway: RealmGateway,
        user_gateway: UserGateway,
    ) -> None:
        self.transaction = transaction
        self.task_gateway = task_gateway
        self.user_gateway = user_gateway

    async def __call__(self, data: RealmCreateDTO) -> RealmCreateResult:
        user = await self.user_gateway.get(data.user_id)

        realm = RealmService().create(
            owner=user,
            name=data.task_name,
            description=data.task_description,
        )

        realm_id = await self.task_gateway.add(realm)
        await self.transaction.commit()
        return RealmCreateResult(realm_id=realm_id)
