import pytest
from unittest.mock import AsyncMock, MagicMock
import uuid

from task_manager.application.interactors.user_register import (
    UserRegisterInteractorImpl,
    UserRegisterDTO,
)
from task_manager.application.exceptions import UsernameTakenExeption
from task_manager.domain.models.user import User, UserId
from task_manager.domain.models.id import IdType


@pytest.fixture
def mock_transaction():
    """Create a mock transaction manager."""
    transaction = AsyncMock()
    transaction.commit = AsyncMock()
    return transaction


@pytest.fixture
def mock_user_gateway():
    """Create a mock user gateway."""
    gateway = AsyncMock()
    return gateway


@pytest.fixture
def mock_encryption_context():
    """Create a mock encryption context."""
    context = MagicMock()
    context.hash = MagicMock(return_value="hashed_password")
    return context


@pytest.fixture
def user_register_interactor(
    mock_transaction, mock_user_gateway, mock_encryption_context
):
    """Create UserRegisterInteractorImpl with mocked dependencies."""
    return UserRegisterInteractorImpl(
        transaction=mock_transaction,
        user_gateway=mock_user_gateway,
        encryption_context=mock_encryption_context,
    )


@pytest.mark.asyncio
async def test_user_register_interactor_success(
    user_register_interactor: UserRegisterInteractorImpl,
    mock_user_gateway,
    mock_encryption_context,
    mock_transaction,
):
    """Test successful user registration."""
    # Setup mocks
    mock_user_gateway.read_by_username.return_value = (
        None  # Username not taken
    )
    user_id = UserId(IdType(uuid.uuid4()))
    mock_user_gateway.add = AsyncMock(return_value=user_id)

    # Execute
    dto = UserRegisterDTO(username="newuser", password="plainpassword")
    result = await user_register_interactor(dto)

    # Verify
    assert result == user_id
    mock_user_gateway.read_by_username.assert_called_once_with("newuser")
    mock_encryption_context.hash.assert_called_once_with("plainpassword")
    mock_user_gateway.add.assert_called_once()
    mock_transaction.commit.assert_called_once()

    # Verify the user passed to add has hashed password
    added_user = mock_user_gateway.add.call_args[0][0]
    assert added_user.username == "newuser"
    assert added_user.password == "hashed_password"
    assert added_user.uid is None


@pytest.mark.asyncio
async def test_user_register_interactor_username_taken(
    user_register_interactor: UserRegisterInteractorImpl,
    mock_user_gateway,
):
    """Test user registration with taken username."""
    # Setup mocks
    existing_user = User(
        uid=UserId(IdType(uuid.uuid4())),
        username="takenuser",
        password="hashed",
    )
    mock_user_gateway.read_by_username.return_value = existing_user

    # Execute and verify exception
    dto = UserRegisterDTO(username="takenuser", password="password")

    with pytest.raises(UsernameTakenExeption):
        await user_register_interactor(dto)

    # Verify add was not called
    mock_user_gateway.add.assert_not_called()
