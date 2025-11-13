from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.application.gateways import UserGateway
from task_manager.domain.models.user import User, UserId


class UserGatewayPostgres(UserGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, pk: UserId) -> User | None:
        return await self.session.get(User, pk)

    async def get_existing(self, pk: UserId) -> User:
        user = await self.session.get(User, pk)
        assert user
        return user

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).filter_by(username=username)
        return await self.session.scalar(stmt)

    async def save(self, user: User) -> UserId:
        self.session.add(user)
        await self.session.flush()
        assert user.uid, "User ID has not been generated on db side"
        return user.uid
