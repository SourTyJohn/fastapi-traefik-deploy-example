from fastapi import HTTPException, status
from pydantic import BaseModel

from dishka.integrations.fastapi import inject, FromDishka

from task_manager.domain.models.user import UserId
from task_manager.application.gateways import UserGateway


class UserMeResponse(BaseModel):
    user_id: UserId
    username: str


@inject
async def route(
    user_id: FromDishka[UserId],
    user_gateway: FromDishka[UserGateway],
) -> UserMeResponse:
    try:
        user = await user_gateway.get(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found"},
        )

    if user.uid is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "User data is invalid"},
        )

    return UserMeResponse(
        user_id=user.uid,
        username=user.username,
    )
