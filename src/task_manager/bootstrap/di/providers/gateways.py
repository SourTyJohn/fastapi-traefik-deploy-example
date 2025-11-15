from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.application.gateways import RealmGateway, UserGateway
from task_manager.adapters.postgres.gateways import (
    RealmGatewayPostgres,
    UserGatewayPostgres,
)


class GatewaysProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user(self, _s: AsyncSession) -> UserGateway:
        return UserGatewayPostgres(_s)

    @provide
    def realm(self, _s: AsyncSession) -> RealmGateway:
        return RealmGatewayPostgres(_s)
