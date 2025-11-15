import pytest
from unittest.mock import AsyncMock
import uuid

from task_manager.application.interactors.realm_add import (
    RealmCreateInteractorImpl,
    RealmCreateDTO,
)
from task_manager.domain.models.realm import RealmId
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
def realm_create_interactor(
    mock_transaction, mock_realm_gateway, mock_user_gateway
):
    """Create RealmCreateInteractorImpl with mocked dependencies."""
    return RealmCreateInteractorImpl(
        transaction=mock_transaction,
        task_gateway=mock_realm_gateway,
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


@pytest.mark.asyncio
async def test_realm_create_interactor_success(
    realm_create_interactor: RealmCreateInteractorImpl,
    mock_user_gateway,
    mock_realm_gateway,
    mock_transaction,
    test_user,
):
    """Test successful realm creation."""
    # Setup mocks
    assert test_user.uid is not None
    mock_user_gateway.get = AsyncMock(return_value=test_user)
    realm_id = RealmId(IdType(uuid.uuid4()))
    mock_realm_gateway.add = AsyncMock(return_value=realm_id)

    # Execute
    dto = RealmCreateDTO(
        user_id=test_user.uid,
        task_name="Test Realm",
        task_description="Test Description",
    )
    result = await realm_create_interactor(dto)

    # Verify
    assert result.realm_id == realm_id
    mock_user_gateway.get.assert_called_once_with(test_user.uid)
    mock_realm_gateway.add.assert_called_once()
    mock_transaction.commit.assert_called_once()

    # Verify the realm passed to add
    added_realm = mock_realm_gateway.add.call_args[0][0]
    assert added_realm.name == "Test Realm"
    assert added_realm.description == "Test Description"
    assert added_realm.owner_uid == test_user.uid
    assert added_realm.uid is None


@pytest.mark.asyncio
async def test_realm_create_interactor_with_none_description(
    realm_create_interactor: RealmCreateInteractorImpl,
    mock_user_gateway,
    mock_realm_gateway,
    test_user,
):
    """Test realm creation with None description."""
    # Setup mocks
    assert test_user.uid is not None
    mock_user_gateway.get = AsyncMock(return_value=test_user)
    realm_id = RealmId(IdType(uuid.uuid4()))
    mock_realm_gateway.add = AsyncMock(return_value=realm_id)

    # Execute
    dto = RealmCreateDTO(
        user_id=test_user.uid,
        task_name="Test Realm",
        task_description="",
    )
    result = await realm_create_interactor(dto)

    # Verify
    assert result.realm_id == realm_id
    added_realm = mock_realm_gateway.add.call_args[0][0]
    assert added_realm.description == ""
