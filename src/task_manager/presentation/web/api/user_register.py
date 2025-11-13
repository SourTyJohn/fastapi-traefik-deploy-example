from fastapi import HTTPException, status
from pydantic import BaseModel

from dishka.integrations.fastapi import inject, FromDishka

from task_manager.application.exceptions import UsernameTakenExeption
from task_manager.application.interactors.user_register import (
    UserRegisterInteractor,
    UserRegisterDTO,
)

from task_manager.presentation.middlewares.bearer_auth import TokenGenerator


class UserRegisterRequest(BaseModel):
    username: str
    password: str


class UserRegisterResponse(BaseModel):
    token: str


@inject
async def route(
    data: UserRegisterRequest,
    register_user: FromDishka[UserRegisterInteractor],
    auth_token_generator: FromDishka[TokenGenerator],
) -> UserRegisterResponse:
    try:
        user_id = await register_user(
            UserRegisterDTO(username=data.username, password=data.password)
        )
    except UsernameTakenExeption:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "username already exists"},
        )

    token = await auth_token_generator(user_id)
    return UserRegisterResponse(token=token.token)
