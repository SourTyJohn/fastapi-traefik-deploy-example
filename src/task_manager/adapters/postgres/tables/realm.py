import uuid

from sqlalchemy import Table, Column, String, UUID, ForeignKey

from task_manager.adapters.postgres.base import metadata, mapper_registry
from task_manager.domain.models.realm import Realm


realm_table = Table(
    "realms",
    metadata,
    Column("uid", UUID, primary_key=True, default=uuid.uuid4),
    Column("owner_uid", ForeignKey("users.uid")),
    Column("name", String),
    Column("description", String),
)


mapper_registry.map_imperatively(Realm, realm_table)
