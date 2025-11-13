from task_manager.domain.models.task import Task
from task_manager.domain.models.user import User
from task_manager.domain.exceptions.user import UserHasNoIdException


class TaskService:
    def create(self, owner: User, name: str, description: str):
        if owner.uid is None:
            raise UserHasNoIdException("User must have an ID to create task")

        return Task(
            uid=None,
            owner_uid=owner.uid,
            name=name,
            description=description,
        )
