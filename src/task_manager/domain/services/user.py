from task_manager.domain.models.user import User


class UserService:
    def register(self, username: str, password: str):
        return User(
            uid=None,
            username=username,
            password=password,
        )
