from pydantic import BaseModel

from dishka.integrations.fastapi import inject, FromDishka

from task_manager.domain.models import UserId
from task_manager.application.interactors.task_add import (
    TaskCreateInteractor,
    TaskCreateDTO,
)


class TaskAddSchema(BaseModel):
    name: str
    description: str


@inject
async def route(
    data: TaskAddSchema,
    user_id: FromDishka[UserId],
    interactor: FromDishka[TaskCreateInteractor],
) -> None:
    await interactor(
        TaskCreateDTO(
            user_id,
            task_name=data.name,
            task_description=data.description,
        )
    )
