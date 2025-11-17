import pytest
from unittest.mock import AsyncMock
import uuid

from task_manager.application.interactors.realm_own_list import (
    RealmOwnListInteractorImpl,
    RealmOwnListDTO,
)
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
def realm_own_list_interactor(
    mock_transaction, mock_realm_gateway, mock_user_gateway
):
    """Create RealmOwnListInteractorImpl with mocked dependencies."""
    return RealmOwnListInteractorImpl(
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
async def test_realm_own_list_interactor_success(
    realm_own_list_interactor: RealmOwnListInteractorImpl,
    mock_user_gateway,
    mock_realm_gateway,
    test_user,
):
    """Test successful listing of owned realms."""
    # Setup mocks
    assert test_user.uid is not None
    mock_user_gateway.get = AsyncMock(return_value=test_user)

    realm1 = Realm(
        uid=RealmId(IdType(uuid.uuid4())),
        owner_uid=test_user.uid,
        name="Realm 1",
        description="Description 1",
    )
    realm2 = Realm(
        uid=RealmId(IdType(uuid.uuid4())),
        owner_uid=test_user.uid,
        name="Realm 2",
        description="Description 2",
    )
    mock_realm_gateway.read = AsyncMock(return_value=[realm1, realm2])

    # Execute
    dto = RealmOwnListDTO(
        user_id=test_user.uid,
        pagination_limit=10,
        pagination_offset=0,
    )
    result = await realm_own_list_interactor(dto)

    # Verify
    assert len(result.realms) == 2
    assert result.realms[0].name == "Realm 1"
    assert result.realms[1].name == "Realm 2"
    mock_user_gateway.get.assert_called_once_with(test_user.uid)
    mock_realm_gateway.read.assert_called_once_with(
        10,
        0,
        owner_uid=test_user.uid,
    )


@pytest.mark.asyncio
async def test_realm_own_list_interactor_with_pagination(
    realm_own_list_interactor: RealmOwnListInteractorImpl,
    mock_user_gateway,
    mock_realm_gateway,
    test_user,
):
    """Test listing with pagination."""
    # Setup mocks
    assert test_user.uid is not None
    mock_user_gateway.get = AsyncMock(return_value=test_user)
    mock_realm_gateway.read = AsyncMock(return_value=[])

    # Execute
    dto = RealmOwnListDTO(
        user_id=test_user.uid,
        pagination_limit=5,
        pagination_offset=10,
    )
    result = await realm_own_list_interactor(dto)

    # Verify
    assert len(result.realms) == 0
    mock_realm_gateway.read.assert_called_once_with(
        5,
        10,
        owner_uid=test_user.uid,
    )


@pytest.mark.asyncio
async def test_realm_own_list_interactor_empty_list(
    realm_own_list_interactor: RealmOwnListInteractorImpl,
    mock_user_gateway,
    mock_realm_gateway,
    test_user,
):
    """Test listing when user has no realms."""
    # Setup mocks
    assert test_user.uid is not None
    mock_user_gateway.get = AsyncMock(return_value=test_user)
    mock_realm_gateway.read = AsyncMock(return_value=[])

    # Execute
    dto = RealmOwnListDTO(
        user_id=test_user.uid,
        pagination_limit=10,
        pagination_offset=0,
    )
    result = await realm_own_list_interactor(dto)

    # Verify
    assert len(result.realms) == 0
