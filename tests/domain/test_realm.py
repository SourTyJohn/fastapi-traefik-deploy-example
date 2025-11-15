import pytest
import uuid

from task_manager.domain.models.realm import Realm, RealmId
from task_manager.domain.models.user import User, UserId
from task_manager.domain.models.id import IdType
from task_manager.domain.services.realm import RealmService
from task_manager.domain.exceptions.user import UserHasNoIdException
from task_manager.domain.exceptions.realm import RealmOwnershipException


@pytest.fixture
def user_with_id():
    """Create a user with an ID."""
    return User(
        uid=UserId(IdType(uuid.uuid4())),
        username="testuser",
        password="hashedpassword",
    )


@pytest.fixture
def user_without_id():
    """Create a user without an ID."""
    return User(
        uid=None,
        username="testuser",
        password="hashedpassword",
    )


@pytest.fixture
def realm(user_with_id):
    """Create a realm owned by user_with_id."""
    return Realm(
        uid=RealmId(IdType(uuid.uuid4())),
        owner_uid=user_with_id.uid,
        name="Test Realm",
        description="Test Description",
    )


def test_realm_service_create(user_with_id):
    """Test RealmService.create creates a realm with correct attributes."""
    service = RealmService()
    name = "My Realm"
    description = "My Description"

    realm = service.create(user_with_id, name, description)

    assert realm.uid is None  # New realm should not have ID yet
    assert realm.owner_uid == user_with_id.uid
    assert realm.name == name
    assert realm.description == description
    assert isinstance(realm, Realm)


def test_realm_service_create_without_description(user_with_id):
    """Test RealmService.create with None description."""
    service = RealmService()

    realm = service.create(user_with_id, "Realm Name", None)

    assert realm.name == "Realm Name"
    assert realm.description is None


def test_realm_service_create_user_without_id(user_without_id):
    """Test RealmService.create raises exception when user has no ID."""
    service = RealmService()

    with pytest.raises(UserHasNoIdException) as exc_info:
        service.create(user_without_id, "Realm Name", "Description")

    assert "User must have an ID to create realm" in str(exc_info.value)


def test_realm_service_check_ownership_success(realm, user_with_id):
    """Test RealmService.check_ownership succeeds when user is owner."""
    service = RealmService()

    # Should not raise exception
    service.check_ownership(realm, user_with_id)


def test_realm_service_check_ownership_user_without_id(realm, user_without_id):
    """Test RealmService.check_ownership raises exception when user has no ID."""
    service = RealmService()

    with pytest.raises(RealmOwnershipException) as exc_info:
        service.check_ownership(realm, user_without_id)

    assert "User must have an ID to check ownership" in str(exc_info.value)


def test_realm_service_check_ownership_different_user(realm, user_with_id):
    """Test RealmService.check_ownership raises exception when user is not owner."""
    service = RealmService()

    # Create a different user
    other_user = User(
        uid=UserId(IdType(uuid.uuid4())),
        username="otheruser",
        password="password",
    )

    with pytest.raises(RealmOwnershipException) as exc_info:
        service.check_ownership(realm, other_user)

    assert "User is not the owner of this realm" in str(exc_info.value)


def test_realm_service_update_success(realm, user_with_id):
    """Test RealmService.update successfully updates realm when user is owner."""
    service = RealmService()
    new_name = "Updated Name"
    new_description = "Updated Description"

    updated_realm = service.update(
        realm, user_with_id, new_name, new_description
    )

    assert updated_realm.name == new_name
    assert updated_realm.description == new_description
    assert updated_realm.uid == realm.uid  # ID should remain the same
    assert (
        updated_realm.owner_uid == realm.owner_uid
    )  # Owner should remain the same


def test_realm_service_update_with_none_description(realm, user_with_id):
    """Test RealmService.update with None description."""
    service = RealmService()

    updated_realm = service.update(realm, user_with_id, "New Name", None)

    assert updated_realm.name == "New Name"
    assert updated_realm.description is None


def test_realm_service_update_user_without_id(realm, user_without_id):
    """Test RealmService.update raises exception when user has no ID."""
    service = RealmService()

    with pytest.raises(RealmOwnershipException):
        service.update(realm, user_without_id, "New Name", "New Description")


def test_realm_service_update_different_user(realm, user_with_id):
    """Test RealmService.update raises exception when user is not owner."""
    service = RealmService()

    # Create a different user
    other_user = User(
        uid=UserId(IdType(uuid.uuid4())),
        username="otheruser",
        password="password",
    )

    with pytest.raises(RealmOwnershipException):
        service.update(realm, other_user, "Hacked Name", "Hacked Description")
