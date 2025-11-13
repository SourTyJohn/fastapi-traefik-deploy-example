from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.application.gateways import TaskGateway, UserGateway
from task_manager.adapters.postgres.gateways import (
    TaskGatewayPostgres,
    UserGatewayPostgres,
)


class GatewaysProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user(self, _s: AsyncSession) -> UserGateway:
        return UserGatewayPostgres(_s)

    @provide
    def task(self, _s: AsyncSession) -> TaskGateway:
        return TaskGatewayPostgres(_s)
