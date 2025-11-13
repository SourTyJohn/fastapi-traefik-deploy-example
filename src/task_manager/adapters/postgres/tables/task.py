import uuid

from sqlalchemy import Table, Column, String, UUID

from task_manager.adapters.postgres.base import metadata, mapper_registry
from task_manager.domain.models.task import Task


tasks_table = Table(
    "tasks",
    metadata,
    Column("uid", UUID, primary_key=True, default=uuid.uuid4),
    Column("name", String),
    Column("description", String),
)


mapper_registry.map_imperatively(Task, tasks_table)
