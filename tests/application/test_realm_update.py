import pytest
from unittest.mock import AsyncMock
import uuid

from task_manager.application.interactors.realm_update import (
    RealmUpdateInteractorImpl,
    RealmUpdateDTO,
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
def realm_update_interactor(mock_transaction, mock_realm_gateway, mock_user_gateway):
    """Create RealmUpdateInteractorImpl with mocked dependencies."""
    return RealmUpdateInteractorImpl(
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
        name="Original Name",
        description="Original Description",
    )


@pytest.mark.asyncio
async def test_realm_update_interactor_success(
    realm_update_interactor: RealmUpdateInteractorImpl,
    mock_realm_gateway,
    mock_user_gateway,
    mock_transaction,
    test_user,
    test_realm,
):
    """Test successful realm update by owner."""
    # Setup mocks
    assert test_user.uid is not None
    mock_realm_gateway.get = AsyncMock(return_value=test_realm)
    mock_user_gateway.get = AsyncMock(return_value=test_user)
    mock_realm_gateway.update = AsyncMock()
    
    # Execute
    dto = RealmUpdateDTO(
        realm_id=test_realm.uid,
        user_id=test_user.uid,
        name="Updated Name",
        description="Updated Description",
    )
    result = await realm_update_interactor(dto)
    
    # Verify
    assert result.name == "Updated Name"
    assert result.description == "Updated Description"
    mock_realm_gateway.get.assert_called_once_with(test_realm.uid)
    mock_user_gateway.get.assert_called_once_with(test_user.uid)
    mock_realm_gateway.update.assert_called_once()
    mock_transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_realm_update_interactor_permission_denied(
    realm_update_interactor: RealmUpdateInteractorImpl,
    mock_realm_gateway,
    mock_user_gateway,
    test_user,
    test_realm,
):
    """Test realm update by non-owner raises PermissionDeniedException."""
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
    dto = RealmUpdateDTO(
        realm_id=test_realm.uid,
        user_id=other_user.uid,
        name="Hacked Name",
        description="Hacked Description",
    )
    
    with pytest.raises(PermissionDeniedException):
        await realm_update_interactor(dto)
    
    # Verify update was not called
    mock_realm_gateway.update.assert_not_called()


@pytest.mark.asyncio
async def test_realm_update_interactor_with_none_description(
    realm_update_interactor: RealmUpdateInteractorImpl,
    mock_realm_gateway,
    mock_user_gateway,
    test_user,
    test_realm,
):
    """Test realm update with None description."""
    # Setup mocks
    assert test_user.uid is not None
    mock_realm_gateway.get = AsyncMock(return_value=test_realm)
    mock_user_gateway.get = AsyncMock(return_value=test_user)
    mock_realm_gateway.update = AsyncMock()
    
    # Execute
    dto = RealmUpdateDTO(
        realm_id=test_realm.uid,
        user_id=test_user.uid,
        name="Updated Name",
        description=None,
    )
    result = await realm_update_interactor(dto)
    
    # Verify
    assert result.name == "Updated Name"
    assert result.description is None

