from task_manager.domain.models.user import User
from task_manager.domain.services.user import UserService


def test_user_service_register():
    """Test UserService.register creates a User with correct attributes."""
    service = UserService()
    username = "testuser"
    password = "testpassword123"

    user = service.register(username, password)

    assert user.uid is None  # New user should not have ID yet
    assert user.username == username
    assert user.password == password
    assert isinstance(user, User)


def test_user_service_register_different_users():
    """Test UserService.register creates different user instances."""
    service = UserService()

    user1 = service.register("user1", "pass1")
    user2 = service.register("user2", "pass2")

    assert user1.username == "user1"
    assert user2.username == "user2"
    assert user1.password == "pass1"
    assert user2.password == "pass2"
    assert user1 is not user2  # Different instances
