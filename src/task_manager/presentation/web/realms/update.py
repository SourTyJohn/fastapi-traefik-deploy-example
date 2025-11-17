from fastapi import HTTPException, Path, status
from pydantic import BaseModel

from dishka.integrations.fastapi import inject, FromDishka

from task_manager.domain.models import RealmId, UserId
from task_manager.application.exceptions import PermissionDeniedException
from task_manager.application.interactors.realm_update import (
    RealmUpdateInteractor,
    RealmUpdateDTO,
)


class RealmUpdateRequest(BaseModel):
    name: str
    description: str | None = None


class RealmUpdateResponse(BaseModel):
    realm_id: RealmId
    owner_id: UserId
    name: str
    description: str | None


@inject
async def route(
    data: RealmUpdateRequest,
    user_id: FromDishka[UserId],
    interactor: FromDishka[RealmUpdateInteractor],
    realm_id: RealmId = Path(..., description="The ID of the realm to update"),
) -> RealmUpdateResponse:
    try:
        realm = await interactor(
            RealmUpdateDTO(
                realm_id=realm_id,
                user_id=user_id,
                name=data.name,
                description=data.description,
            )
        )
    except PermissionDeniedException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Permission denied. Only the owner can update this realm."
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Realm not found"},
        )

    if realm.uid is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Realm data is invalid"},
        )

    return RealmUpdateResponse(
        realm_id=realm.uid,
        owner_id=realm.owner_uid,
        name=realm.name,
        description=realm.description,
    )
