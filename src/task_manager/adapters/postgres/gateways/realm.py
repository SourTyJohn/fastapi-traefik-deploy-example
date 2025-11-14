from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from task_manager.application.gateways import RealmGateway
from task_manager.domain.models.realm import Realm, RealmId


class RealmGatewayPostgres(RealmGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, pk: RealmId) -> Realm:
        return await self.session.get_one(Realm, pk)

    async def add(self, realm: Realm) -> RealmId:
        self.session.add(realm)
        await self.session.flush()
        assert realm.uid
        return realm.uid

    async def update(self, realm: Realm):
        self.session.add(realm)
        await self.session.flush()

    async def delete(self, realm: Realm) -> None:
        await self.session.delete(realm)
        await self.session.flush()

    async def read(
        self,
        limit: int | None = None,
        offset: int | None = None,
        **filters,
    ) -> Sequence[Realm]:
        stmt = select(Realm).filter_by(**filters)

        if limit is not None:
            stmt = stmt.limit(limit)

        if offset is not None:
            stmt = stmt.offset(offset)

        return (await self.session.scalars(stmt)).all()
