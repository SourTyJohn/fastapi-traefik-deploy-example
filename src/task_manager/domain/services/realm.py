from task_manager.domain.models.realm import Realm
from task_manager.domain.models.user import User
from task_manager.domain.exceptions.user import UserHasNoIdException


class RealmService:
    def create(self, owner: User, name: str, description: str | None):
        if owner.uid is None:
            raise UserHasNoIdException("User must have an ID to create realm")

        return Realm(
            uid=None,
            owner_uid=owner.uid,
            name=name,
            description=description,
        )
