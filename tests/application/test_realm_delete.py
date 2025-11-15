import pytest
from unittest.mock import AsyncMock
import uuid

from task_manager.application.interactors.realm_delete import (
    RealmDeleteInteractorImpl,
)
from task_manager.application.exceptions import PermissionDeniedException
from task_manager.domain.models.realm import Realm, RealmId
from task_manager.domain.models.user import User, UserId
from task_manager.domain.models.id import IdType


@pytest.fixture
def mock_transaction():
    """Create a mock transaction manager."""
    transaction = AsyncMock()
    transaction.commit = AsyncMock()
    return transaction


@pytest.fixture
def mock_realm_gateway():
    """Create a mock realm gateway."""
    gateway = AsyncMock()
    return gateway


@pytest.fixture
def mock_user_gateway():
    """Create a mock user gateway."""
    gateway = AsyncMock()
    return gateway


@pytest.fixture
def realm_delete_interactor(
    mock_transaction, mock_realm_gateway, mock_user_gateway
):
    """Create RealmDeleteInteractorImpl with mocked dependencies."""
    return RealmDeleteInteractorImpl(
        transaction=mock_transaction,
        realm_gateway=mock_realm_gateway,
        user_gateway=mock_user_gateway,
    )


@pytest.fixture
def test_user():
    """Create a test user."""
    return User(
        uid=UserId(IdType(uuid.uuid4())),
        username="testuser",
        password="hashedpassword",
    )


@pytest.fixture
def test_realm(test_user):
    """Create a test realm owned by test_user."""
    return Realm(
        uid=RealmId(IdType(uuid.uuid4())),
        owner_uid=test_user.uid,
        name="Test Realm",
        description="Test Description",
    )


@pytest.mark.asyncio
async def test_realm_delete_interactor_success(
    realm_delete_interactor: RealmDeleteInteractorImpl,
    mock_realm_gateway,
    mock_user_gateway,
    mock_transaction,
    test_user,
    test_realm,
):
    """Test successful realm deletion by owner."""
    # Setup mocks
    assert test_user.uid is not None
    mock_realm_gateway.get = AsyncMock(return_value=test_realm)
    mock_user_gateway.get = AsyncMock(return_value=test_user)
    mock_realm_gateway.delete = AsyncMock()

    # Execute
    await realm_delete_interactor(test_realm.uid, test_user.uid)

    # Verify
    mock_realm_gateway.get.assert_called_once_with(test_realm.uid)
    mock_user_gateway.get.assert_called_once_with(test_user.uid)
    mock_realm_gateway.delete.assert_called_once_with(test_realm)
    mock_transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_realm_delete_interactor_permission_denied(
    realm_delete_interactor: RealmDeleteInteractorImpl,
    mock_realm_gateway,
    mock_user_gateway,
    test_user,
    test_realm,
):
    """Test realm deletion by non-owner raises PermissionDeniedException."""
    # Setup mocks
    other_user = User(
        uid=UserId(IdType(uuid.uuid4())),
        username="otheruser",
        password="password",
    )
    assert other_user.uid is not None
    mock_realm_gateway.get = AsyncMock(return_value=test_realm)
    mock_user_gateway.get = AsyncMock(return_value=other_user)

    # Execute and verify exception
    with pytest.raises(PermissionDeniedException):
        await realm_delete_interactor(test_realm.uid, other_user.uid)

    # Verify delete was not called
    mock_realm_gateway.delete.assert_not_called()
