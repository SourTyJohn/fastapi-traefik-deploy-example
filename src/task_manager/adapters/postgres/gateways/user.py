from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.application.gateways import UserGateway
from task_manager.domain.models.user import User, UserId


class UserGatewayPostgres(UserGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, pk: UserId) -> User:
        return await self.session.get_one(User, pk)

    async def add(self, user: User) -> UserId:
        self.session.add(user)
        await self.session.flush()
        assert user.uid, "ID has not been generated on DB side"
        return user.uid

    async def update(self, user: User) -> None:
        raise NotImplementedError

    async def delete(self, user: User) -> None:
        raise NotImplementedError

    async def read_by_username(self, username: str) -> User | None:
        stmt = select(User).filter_by(username=username)
        return await self.session.scalar(stmt)
