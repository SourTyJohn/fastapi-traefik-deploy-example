from task_manager.domain.models.realm import Realm
from task_manager.domain.models.user import User
from task_manager.domain.exceptions.user import UserHasNoIdException
from task_manager.domain.exceptions.realm import RealmOwnershipException


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

    def check_ownership(self, realm: Realm, user: User) -> None:
        """Check if the user is the owner of the realm.

        Raises RealmOwnershipException if the user is not the owner.
        """
        if user.uid is None:
            raise RealmOwnershipException(
                "User must have an ID to check ownership"
            )

        if realm.owner_uid != user.uid:
            raise RealmOwnershipException(
                "User is not the owner of this realm"
            )

    def update(self, realm: Realm, user: User, name: str, description: str | None) -> Realm:
        """Update realm with new name and description.

        Checks ownership before updating.
        Raises RealmOwnershipException if the user is not the owner.
        """
        self.check_ownership(realm, user)

        realm.name = name
        realm.description = description

        return realm
