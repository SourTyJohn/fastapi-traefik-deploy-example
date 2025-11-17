from fastapi import HTTPException, Path, status

from dishka.integrations.fastapi import inject, FromDishka

from task_manager.domain.models import RealmId, UserId
from task_manager.application.exceptions import PermissionDeniedException
from task_manager.application.interactors.realm_delete import (
    RealmDeleteInteractor,
)


@inject
async def route(
    user_id: FromDishka[UserId],
    interactor: FromDishka[RealmDeleteInteractor],
    realm_id: RealmId = Path(..., description="The ID of the realm to delete"),
) -> dict:
    try:
        await interactor(realm_id, user_id)
    except PermissionDeniedException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Permission denied. Only the owner can delete this realm."
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Realm not found"},
        )

    return {"message": "Realm deleted successfully"}
