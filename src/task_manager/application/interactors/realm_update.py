from typing import Protocol
from abc import abstractmethod
from dataclasses import dataclass

from task_manager.application.common import AsyncTransactionManager
from task_manager.application.gateways import RealmGateway, UserGateway
from task_manager.application.exceptions import PermissionDeniedException
from task_manager.domain.models import Realm, RealmId, UserId
from task_manager.domain.services.realm import RealmService
from task_manager.domain.exceptions.realm import RealmOwnershipException


@dataclass
class RealmUpdateDTO:
    realm_id: RealmId
    user_id: UserId
    name: str
    description: str | None


class RealmUpdateInteractor(Protocol):
    @abstractmethod
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        realm_gateway: RealmGateway,
        user_gateway: UserGateway,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, data: RealmUpdateDTO) -> Realm:
        raise NotImplementedError


class RealmUpdateInteractorImpl(RealmUpdateInteractor):
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        realm_gateway: RealmGateway,
        user_gateway: UserGateway,
    ) -> None:
        self.transaction = transaction
        self.realm_gateway = realm_gateway
        self.user_gateway = user_gateway

    async def __call__(self, data: RealmUpdateDTO) -> Realm:
        realm = await self.realm_gateway.get(data.realm_id)
        user = await self.user_gateway.get(data.user_id)

        try:
            RealmService().update(realm, user, data.name, data.description)
        except RealmOwnershipException:
            raise PermissionDeniedException()

        await self.realm_gateway.update(realm)
        await self.transaction.commit()

        return realm

