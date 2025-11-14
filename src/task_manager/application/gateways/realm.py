from typing import Protocol, Sequence
from abc import abstractmethod

from task_manager.application.common import AsyncTransactionManager
from task_manager.domain.models import Realm, RealmId


class RealmGateway(Protocol):
    @abstractmethod
    def __init__(self, session: AsyncTransactionManager) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, pk: RealmId) -> Realm:
        raise NotImplementedError

    @abstractmethod
    async def add(self, realm: Realm) -> RealmId:
        raise NotImplementedError

    @abstractmethod
    async def update(self, realm: Realm) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, realm: Realm) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read(
        self,
        limit: int | None = None,
        offset: int | None = None,
        **filters,
    ) -> Sequence[Realm]:
        raise NotImplementedError
