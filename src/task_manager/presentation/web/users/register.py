from fastapi import HTTPException, status
from pydantic import BaseModel, SecretStr, Field

from dishka.integrations.fastapi import inject, FromDishka

from task_manager.domain.models.user import UserId
from task_manager.application.exceptions import UsernameTakenExeption
from task_manager.application.interactors.user_register import (
    UserRegisterInteractor,
    UserRegisterDTO,
)

from task_manager.presentation.middlewares.bearer_auth import TokenGenerator


class UserRegisterRequest(BaseModel):
    username: str = Field(min_length=6, max_length=16)
    password: SecretStr = Field(
        min_length=6,
        max_length=32,
        examples=["secret_password"],
    )


class UserRegisterResponse(BaseModel):
    user_id: UserId
    token: str = Field(description="random_api_bearer_token_key")


@inject
async def route(
    data: UserRegisterRequest,
    register_user: FromDishka[UserRegisterInteractor],
    auth_token_generator: FromDishka[TokenGenerator],
) -> UserRegisterResponse:
    try:
        user_id = await register_user(
            UserRegisterDTO(
                username=data.username,
                password=data.password.get_secret_value(),
            )
        )
    except UsernameTakenExeption:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "username already exists"},
        )

    token = await auth_token_generator(user_id)

    return UserRegisterResponse(
        user_id=user_id,
        token=token.token,
    )
