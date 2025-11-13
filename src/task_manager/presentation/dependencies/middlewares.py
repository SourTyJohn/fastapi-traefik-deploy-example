from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from dishka import Provider, Scope, provide

from task_manager.config import Config
from task_manager.presentation.middlewares.bearer_auth import (
    UserIdBearerProvider,
    TokenGateway,
    TokenGatewayPostgres,
    TokenGenerator,
)
from task_manager.domain.models.user import UserId


class MiddlewaresProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def token_gateway(self, session: AsyncSession) -> TokenGateway:
        return TokenGatewayPostgres(session)

    @provide
    async def token_generator(
        self,
        session: AsyncSession,
        token_gateway: TokenGateway,
        config: Config,
    ) -> TokenGenerator:
        auth_config = config.auth
        return TokenGenerator(
            session,
            token_gateway=token_gateway,
            expire_timedelta=auth_config.TOKEN_EXPIRE_TIMEDELTA,
        )

    @provide
    async def user_id(
        self,
        request: Request,
        session: AsyncSession,
        token_gateway: TokenGateway,
        config: Config,
    ) -> UserId:
        auth_config = config.auth
        provider = UserIdBearerProvider(
            request,
            session=session,
            token_gateway=token_gateway,
            header_name=auth_config.TOKEN_HEADER_NAME,
            auth_scheme=auth_config.TOKEN_AUTH_SCHEME,
        )
        return await provider()
