import pytest
from unittest.mock import AsyncMock, MagicMock
import uuid

from task_manager.application.interactors.user_login import (
    UserLoginInteractorImpl,
)
from task_manager.application.exceptions import InvalidCredentialsException
from task_manager.domain.models.user import User, UserId
from task_manager.domain.models.id import IdType


@pytest.fixture
def mock_transaction():
    """Create a mock transaction manager."""
    transaction = AsyncMock()
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
    return context


@pytest.fixture
def user_login_interactor(mock_transaction, mock_user_gateway, mock_encryption_context):
    """Create UserLoginInteractorImpl with mocked dependencies."""
    return UserLoginInteractorImpl(
        transaction=mock_transaction,
        user_gateway=mock_user_gateway,
        encryption_context=mock_encryption_context,
    )


@pytest.mark.asyncio
async def test_user_login_interactor_success(
    user_login_interactor: UserLoginInteractorImpl,
    mock_user_gateway,
    mock_encryption_context,
):
    """Test successful user login."""
    # Setup mocks
    user_id = UserId(IdType(uuid.uuid4()))
    user = User(
        uid=user_id,
        username="testuser",
        password="hashed_password",
    )
    mock_user_gateway.read_by_username = AsyncMock(return_value=user)
    mock_encryption_context.verify = MagicMock(return_value=True)
    
    # Execute
    result = await user_login_interactor("testuser", "plainpassword")
    
    # Verify
    assert result == user_id
    mock_user_gateway.read_by_username.assert_called_once_with("testuser")
    mock_encryption_context.verify.assert_called_once_with("plainpassword", "hashed_password")


@pytest.mark.asyncio
async def test_user_login_interactor_user_not_found(
    user_login_interactor: UserLoginInteractorImpl,
    mock_user_gateway,
):
    """Test login with non-existent user."""
    # Setup mocks
    mock_user_gateway.read_by_username = AsyncMock(return_value=None)
    
    # Execute and verify exception
    with pytest.raises(InvalidCredentialsException):
        await user_login_interactor("nonexistent", "password")


@pytest.mark.asyncio
async def test_user_login_interactor_invalid_password(
    user_login_interactor: UserLoginInteractorImpl,
    mock_user_gateway,
    mock_encryption_context,
):
    """Test login with invalid password."""
    # Setup mocks
    user_id = UserId(IdType(uuid.uuid4()))
    user = User(
        uid=user_id,
        username="testuser",
        password="hashed_password",
    )
    mock_user_gateway.read_by_username = AsyncMock(return_value=user)
    mock_encryption_context.verify = MagicMock(return_value=False)
    
    # Execute and verify exception
    with pytest.raises(InvalidCredentialsException):
        await user_login_interactor("testuser", "wrongpassword")
    
    mock_encryption_context.verify.assert_called_once_with("wrongpassword", "hashed_password")


@pytest.mark.asyncio
async def test_user_login_interactor_user_without_id(
    user_login_interactor: UserLoginInteractorImpl,
    mock_user_gateway,
    mock_encryption_context,
):
    """Test login with user that has no ID."""
    # Setup mocks
    user = User(
        uid=None,
        username="testuser",
        password="hashed_password",
    )
    mock_user_gateway.read_by_username = AsyncMock(return_value=user)
    mock_encryption_context.verify = MagicMock(return_value=True)
    
    # Execute and verify exception
    with pytest.raises(InvalidCredentialsException):
        await user_login_interactor("testuser", "password")

