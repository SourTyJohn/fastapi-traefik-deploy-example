import uuid

from sqlalchemy import Table, Column, String, UUID

from task_manager.adapters.postgres.base import metadata, mapper_registry
from task_manager.domain.models.user import User


users_table = Table(
    "users",
    metadata,
    Column("uid", UUID, primary_key=True, default=uuid.uuid4),
    Column("username", String),
    Column("password", String),
)


mapper_registry.map_imperatively(User, users_table)
