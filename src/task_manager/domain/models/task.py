from dataclasses import dataclass
from typing import NewType

from task_manager.domain.models.id import IdType
from task_manager.domain.models.user import UserId


TaskId = NewType("TaskId", IdType)


@dataclass
class Task:
    uid: TaskId | None
    owner_uid: UserId
    name: str
    description: str
