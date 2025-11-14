from pydantic import BaseModel

from dishka.integrations.fastapi import inject, FromDishka

from task_manager.domain.models import UserId
from task_manager.application.interactors.realm_add import (
    RealmCreateInteractor,
    RealmCreateDTO,
    RealmCreateResult,
)


class RealmAddRequest(BaseModel):
    name: str
    description: str


@inject
async def route(
    data: RealmAddRequest,
    user_id: FromDishka[UserId],
    interactor: FromDishka[RealmCreateInteractor],
) -> RealmCreateResult:
    return await interactor(
        RealmCreateDTO(
            user_id,
            task_name=data.name,
            task_description=data.description,
        )
    )
