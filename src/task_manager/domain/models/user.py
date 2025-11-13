from dataclasses import dataclass
from typing import NewType

from task_manager.domain.models.id import IdType


UserId = NewType("UserId", IdType)


@dataclass
class User:
    uid: UserId | None
    username: str
    password: str
