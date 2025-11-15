import pytest
from unittest.mock import AsyncMock
import uuid

from task_manager.application.interactors.realm_get import (
    RealmGetInteractorImpl,
)
from task_manager.application.exceptions import PermissionDeniedException
from task_manager.domain.models.realm import Realm, RealmId
from task_manager.domain.models.user import User, UserId
from task_manager.domain.models.id import IdType


@pytest.fixture
def mock_transaction():
    """Create a mock transaction manager."""
    transaction = AsyncMock()
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
def realm_get_interactor(
    mock_transaction, mock_realm_gateway, mock_user_gateway
):
    """Create RealmGetInteractorImpl with mocked dependencies."""
    return RealmGetInteractorImpl(
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
async def test_realm_get_interactor_success(
    realm_get_interactor: RealmGetInteractorImpl,
    mock_realm_gateway,
    mock_user_gateway,
    test_user,
    test_realm,
):
    """Test successful realm retrieval by owner."""
    # Setup mocks
    assert test_user.uid is not None
    mock_realm_gateway.get = AsyncMock(return_value=test_realm)
    mock_user_gateway.get = AsyncMock(return_value=test_user)

    # Execute
    result = await realm_get_interactor(test_realm.uid, test_user.uid)

    # Verify
    assert result == test_realm
    mock_realm_gateway.get.assert_called_once_with(test_realm.uid)
    mock_user_gateway.get.assert_called_once_with(test_user.uid)


@pytest.mark.asyncio
async def test_realm_get_interactor_permission_denied(
    realm_get_interactor: RealmGetInteractorImpl,
    mock_realm_gateway,
    mock_user_gateway,
    test_user,
    test_realm,
):
    """Test realm retrieval by non-owner raises PermissionDeniedException."""
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
        await realm_get_interactor(test_realm.uid, other_user.uid)
