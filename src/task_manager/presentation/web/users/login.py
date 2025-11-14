from fastapi import HTTPException, status
from pydantic import BaseModel, SecretStr, Field

from dishka.integrations.fastapi import inject, FromDishka

from task_manager.domain.models.user import UserId
from task_manager.application.exceptions import InvalidCredentialsException
from task_manager.application.interactors.user_login import (
    UserLoginInteractor,
)
from task_manager.presentation.middlewares.bearer_auth import TokenGenerator


class UserLoginRequest(BaseModel):
    username: str = Field(min_length=6, max_length=16)
    password: SecretStr = Field(
        min_length=6,
        max_length=32,
        examples=["secret_password"],
    )


class UserLoginResponse(BaseModel):
    user_id: UserId
    token: str = Field(description="api_bearer_token_key")


@inject
async def route(
    data: UserLoginRequest,
    login_user: FromDishka[UserLoginInteractor],
    auth_token_generator: FromDishka[TokenGenerator],
) -> UserLoginResponse:
    try:
        user_id = await login_user(
            username=data.username,
            password=data.password.get_secret_value(),
        )
    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid username or password"},
        )

    token = await auth_token_generator(user_id)

    return UserLoginResponse(
        user_id=user_id,
        token=token.token,
    )
