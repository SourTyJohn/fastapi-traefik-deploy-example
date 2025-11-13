from datetime import timedelta

from task_manager.presentation.middlewares.bearer_auth import (
    TokenGateway,
    TokenService,
    Token,
)
from task_manager.application.common import AsyncTransactionManager
from task_manager.domain.models.user import UserId


class TokenGenerator:
    def __init__(
        self,
        session: AsyncTransactionManager,
        token_gateway: TokenGateway,
        expire_timedelta: timedelta,
    ) -> None:
        self.session = session
        self.token_gateway = token_gateway
        self.expire_timedelta = expire_timedelta

    async def __call__(self, user_id: UserId) -> Token:
        token = TokenService().generate(user_id, self.expire_timedelta)
        await self.token_gateway.save(token)
        await self.session.commit()
        return token
