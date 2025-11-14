from dataclasses import dataclass
from typing import NewType, Optional

from task_manager.domain.models.id import IdType
from task_manager.domain.models.user import UserId


RealmId = NewType("RealmId", IdType)


@dataclass
class Realm:
    uid: RealmId | None
    owner_uid: UserId
    name: str
    description: Optional[str]
