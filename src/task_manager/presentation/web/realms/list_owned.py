from dishka.integrations.fastapi import inject, FromDishka

from task_manager.domain.models import UserId
from task_manager.application.interactors.realm_own_list import (
    RealmOwnListInteractor,
    RealmOwnListDTO,
    RealmOwnListResult,
)
from task_manager.presentation.web.depends import PaginationDep


@inject
async def route(
    interactor: FromDishka[RealmOwnListInteractor],
    user_id: FromDishka[UserId],
    pagination: PaginationDep,
) -> RealmOwnListResult:
    return await interactor(
        RealmOwnListDTO(
            user_id=user_id,
            pagination_limit=pagination.limit,
            pagination_offset=pagination.offset,
        )
    )
