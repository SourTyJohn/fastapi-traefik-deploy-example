from fastapi import Request, HTTPException, status

from task_manager.presentation.middlewares.id_middleware import (
    CurrentUserIdProvider,
)
from task_manager.presentation.middlewares.bearer_auth.gateway import (
    TokenGateway,
)
from task_manager.presentation.middlewares.bearer_auth.token import (
    TokenService,
)
from task_manager.application.common import AsyncTransactionManager
from task_manager.domain.models.user import UserId


class UserIdBearerProvider(CurrentUserIdProvider):
    def __init__(
        self,
        request: Request,
        session: AsyncTransactionManager,
        token_gateway: TokenGateway,
        header_name: str,
        auth_scheme: str,
    ) -> None:
        self.request = request
        self.session = session
        self.key_header_name = header_name
        self.auth_scheme = auth_scheme
        self.token_gateway = token_gateway

    async def __call__(self) -> UserId:
        auth_header = self.request.headers.get(self.key_header_name, None)

        try:
            if auth_header is None:
                raise ValueError("Not authenticated")

            splitted_header = auth_header.split()
            if len(splitted_header) != 2:
                raise ValueError("Invalid authentication scheme")

            scheme, token = splitted_header
            if scheme != self.auth_scheme:
                raise ValueError("Invalid authentication scheme")

            db_token = await self.token_gateway.get_by_token(token)
            if db_token is None:
                raise ValueError("Invalid token")

            if TokenService().is_expired(db_token):
                await self.token_gateway.delete(db_token)
                await self.session.commit()
                raise ValueError("Expired token")

        except ValueError as _e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=_e.args
            )

        return db_token.owner_uid
