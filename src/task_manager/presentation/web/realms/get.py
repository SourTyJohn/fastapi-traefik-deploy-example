from fastapi import HTTPException, Path, status
from pydantic import BaseModel

from dishka.integrations.fastapi import inject, FromDishka

from task_manager.domain.models import RealmId, UserId
from task_manager.application.exceptions import PermissionDeniedException
from task_manager.application.interactors.realm_get import RealmGetInteractor


class RealmGetResponse(BaseModel):
    realm_id: RealmId
    owner_id: UserId
    name: str
    description: str | None


@inject
async def route(
    user_id: FromDishka[UserId],
    interactor: FromDishka[RealmGetInteractor],
    realm_id: RealmId = Path(
        ..., description="The ID of the realm to retrieve"
    ),
) -> RealmGetResponse:
    try:
        realm = await interactor(realm_id, user_id)
    except PermissionDeniedException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Permission denied. Only the owner can access this realm."
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

    return RealmGetResponse(
        realm_id=realm.uid,
        owner_id=realm.owner_uid,
        name=realm.name,
        description=realm.description,
    )
