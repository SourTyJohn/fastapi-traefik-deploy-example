from typing import Protocol
from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from task_manager.application.common.transaction import AsyncTransactionManager
from task_manager.presentation.middlewares.bearer_auth.token import (
    Token,
    TokenId,
)


class TokenGateway(Protocol):
    @abstractmethod
    def __init__(self, session: AsyncTransactionManager) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_token(self, token: str) -> Token | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, token: Token) -> TokenId:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, token: Token) -> None:
        raise NotImplementedError


class TokenGatewayPostgres(TokenGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_token(self, token: str) -> Token | None:
        stmt = select(Token).filter_by(token=token)
        return await self.session.scalar(stmt)

    async def save(self, token: Token) -> TokenId:
        self.session.add(token)
        await self.session.flush()
        assert token.uid, "Token ID has not been generated on db side"
        return token.uid

    async def delete(self, token: Token) -> None:
        await self.session.delete(token)
        await self.session.flush()
