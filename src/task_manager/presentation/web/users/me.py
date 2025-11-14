from dishka.integrations.fastapi import inject, FromDishka

from task_manager.domain.models.user import UserId, User
from task_manager.application.gateways import UserGateway


@inject
async def route(
    user_id: FromDishka[UserId],
    user_gateway: FromDishka[UserGateway],
) -> User:
    return await user_gateway.get(user_id)
