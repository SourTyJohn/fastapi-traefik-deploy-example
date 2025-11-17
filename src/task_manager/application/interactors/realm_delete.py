from typing import Protocol
from abc import abstractmethod

from task_manager.application.common import AsyncTransactionManager
from task_manager.application.gateways import RealmGateway, UserGateway
from task_manager.application.exceptions import PermissionDeniedException
from task_manager.domain.models import RealmId, UserId
from task_manager.domain.services.realm import RealmService
from task_manager.domain.exceptions.realm import RealmOwnershipException


class RealmDeleteInteractor(Protocol):
    @abstractmethod
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        realm_gateway: RealmGateway,
        user_gateway: UserGateway,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, realm_id: RealmId, user_id: UserId) -> None:
        raise NotImplementedError


class RealmDeleteInteractorImpl(RealmDeleteInteractor):
    def __init__(
        self,
        transaction: AsyncTransactionManager,
        realm_gateway: RealmGateway,
        user_gateway: UserGateway,
    ) -> None:
        self.transaction = transaction
        self.realm_gateway = realm_gateway
        self.user_gateway = user_gateway

    async def __call__(self, realm_id: RealmId, user_id: UserId) -> None:
        realm = await self.realm_gateway.get(realm_id)
        user = await self.user_gateway.get(user_id)

        try:
            RealmService().check_ownership(realm, user)
        except RealmOwnershipException:
            raise PermissionDeniedException()

        await self.realm_gateway.delete(realm)
        await self.transaction.commit()
